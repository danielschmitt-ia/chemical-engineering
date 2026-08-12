import numpy as np
import matplotlib.pyplot as plt
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

from reator_digital_twin import ReatorCSTR, carregar_config

if __name__ == "__main__":
    print("🚀 Executando simulação integrada...")
    reator = ReatorCSTR(carregar_config("configs/reator_padrao.yaml"))
    t1, T_seguro = reator.simular_runaway(UA_operacao=50000.0)
    _, T_critico = reator.simular_runaway(UA_operacao=32000.0)
    t2, hist_T_mpc, hist_Tj_mpc, hist_CA_mpc = reator.rodar_mpc()

    X_dados = (hist_T_mpc + np.random.normal(0, 0.4, size=len(hist_T_mpc))).reshape(-1, 1)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_dados)
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, hist_CA_mpc, test_size=0.2, random_state=42)

    # Ensemble via bootstrap: em vez de uma única rede, treina várias em reamostragens dos
    # dados e usa a dispersão entre elas como estimativa de incerteza (soft sensor
    # "uncertainty-aware"), para sinalizar quando a estimativa de C_A é pouco confiável.
    n_ensemble = 15
    rng = np.random.default_rng(42)
    preds_ensemble = np.zeros((n_ensemble, len(X_scaled)))
    for m in range(n_ensemble):
        idx_boot = rng.integers(0, len(X_train), size=len(X_train))
        modelo = MLPRegressor(hidden_layer_sizes=(15, 10), max_iter=2000, random_state=m)
        modelo.fit(X_train[idx_boot], y_train[idx_boot])
        preds_ensemble[m] = modelo.predict(X_scaled)
    concentracao_predita = preds_ensemble.mean(axis=0)
    concentracao_incerteza = preds_ensemble.std(axis=0)
    print(f"📈 Soft sensor: incerteza média (±1 desvio-padrão do ensemble) = {concentracao_incerteza.mean():.3f} mol/L")

    print("🔎 Executando cenário de fouling com detecção de falha...")
    t3, T_falha, Tj_falha, UA_real_falha, residuo_falha, tempo_deteccao = reator.rodar_mpc_com_deteccao_falha()
    if tempo_deteccao is not None:
        print(f"⚠️  Degradação de UA detectada em t = {tempo_deteccao:.2f} min "
              f"(UA real na detecção ≈ {UA_real_falha[np.searchsorted(t3, tempo_deteccao)]:.0f})")
    else:
        print("✅ Nenhuma falha detectada no horizonte simulado.")

    print("🛡️  Executando cenário de interlock (SIS) sob descasamento de modelo...")
    t4, T_sem_sis, _, _, _ = reator.simular_interlock_seguranca(usar_sis=False)
    _, T_com_sis, Tj_mpc_sis, sis_ativo, tempo_trip = reator.simular_interlock_seguranca(usar_sis=True)
    if tempo_trip is not None:
        print(f"🚨 SIS disparou em t = {tempo_trip:.2f} min "
              f"(pico sem SIS: {T_sem_sis.max():.0f} K | pico com SIS: {T_com_sis.max():.0f} K)")
    else:
        print("✅ SIS não precisou intervir no horizonte simulado.")

    print("💰 Executando Economic MPC (otimização direta de lucro)...")
    t5, T_economico, Tj_economico, CA_economico, lucro_acumulado = reator.rodar_mpc_economico(tempo_total=25)
    print(f"💵 Lucro acumulado (Economic MPC, 25 min): ${lucro_acumulado[-1]:.0f} "
          f"| temperatura de operação encontrada ≈ {T_economico[-5:].mean():.1f} K "
          f"(setpoint fixo do MPC de rastreamento: {reator.T_alvo:.0f} K)")

    fig1, ax1 = plt.subplots(figsize=(10, 5))
    ax1.plot(t1, T_seguro, label='Seguro')
    ax1.plot(t1, T_critico, '--', label='Runaway')
    ax1.set_title('Fuga Térmica (Runaway) — integração RK45')
    ax1.set_xlabel('Tempo (min)'); ax1.set_ylabel('Temperatura (K)')
    ax1.legend(); ax1.grid(True)
    fig1.tight_layout(); fig1.savefig('estabilidade_runaway.png', dpi=150)

    fig2, axs2 = plt.subplots(2, 1, figsize=(10, 8))
    axs2[0].plot(t2, hist_T_mpc, color='purple', label='T (MPC)')
    axs2[0].axhline(y=reator.T_alvo, color='black', linestyle=':', label='Setpoint')
    axs2[0].axhline(y=reator.T_max_seguro, color='red', linestyle='--', label='Teto de segurança')
    axs2[0].set_title('MPC com restrições de segurança (temperatura e taxa do atuador)')
    axs2[0].legend(); axs2[0].grid(True)

    axs2[1].plot(t2, hist_CA_mpc, label='Real')
    axs2[1].plot(t2, concentracao_predita, '--', label='IA (soft sensor, média do ensemble)')
    axs2[1].fill_between(t2, concentracao_predita - 2 * concentracao_incerteza,
                          concentracao_predita + 2 * concentracao_incerteza,
                          color='orange', alpha=0.2, label='Incerteza (±2 desvios-padrão)')
    axs2[1].set_title('Soft Sensor com Quantificação de Incerteza (Ensemble)')
    axs2[1].legend(); axs2[1].grid(True)
    fig2.tight_layout(); fig2.savefig('mpc_softsensor.png', dpi=150)

    fig3, axs3 = plt.subplots(2, 1, figsize=(10, 8))
    axs3[0].plot(t3, UA_real_falha, color='darkorange', label='UA real (fouling)')
    axs3[0].axhline(y=50000.0, color='gray', linestyle=':', label='UA nominal do modelo')
    if tempo_deteccao is not None:
        axs3[0].axvline(x=tempo_deteccao, color='red', linestyle='--', label='Falha detectada')
    axs3[0].set_title('Degradação simulada do coeficiente de troca térmica (UA)')
    axs3[0].legend(); axs3[0].grid(True)

    axs3[1].plot(t3, residuo_falha, color='crimson', label='Resíduo (EWMA)')
    axs3[1].axhline(y=0.4, color='black', linestyle=':', label='Limiar de alarme')
    if tempo_deteccao is not None:
        axs3[1].axvline(x=tempo_deteccao, color='red', linestyle='--')
    axs3[1].set_title('Detecção de Falha por Resíduo do Gêmeo Digital')
    axs3[1].legend(); axs3[1].grid(True)
    fig3.tight_layout(); fig3.savefig('deteccao_falha.png', dpi=150)

    fig4, ax4 = plt.subplots(figsize=(10, 5))
    ax4.plot(t4, T_sem_sis, '--', color='firebrick', label='Sem SIS (só MPC, modelo desatualizado)')
    ax4.plot(t4, T_com_sis, color='seagreen', label='Com SIS (interlock independente)')
    ax4.axhline(y=reator.T_trip_sis, color='black', linestyle=':', label='Setpoint do trip')
    if tempo_trip is not None:
        ax4.axvline(x=tempo_trip, color='red', linestyle='--', label='SIS disparou')
    ax4.set_title('Camada de Proteção Independente (SIS) sob Descasamento de Modelo')
    ax4.set_xlabel('Tempo (min)'); ax4.set_ylabel('Temperatura (K)')
    ax4.legend(); ax4.grid(True)
    fig4.tight_layout(); fig4.savefig('interlock_seguranca.png', dpi=150)

    fig5, axs5 = plt.subplots(2, 1, figsize=(10, 8))
    axs5[0].plot(t5, T_economico, color='teal', label='T (Economic MPC)')
    axs5[0].axhline(y=reator.T_alvo, color='black', linestyle=':', label='Setpoint fixo (MPC de rastreamento)')
    axs5[0].axhline(y=reator.T_max_seguro, color='red', linestyle='--', label='Teto de segurança')
    axs5[0].set_title('Economic MPC: temperatura encontrada ao otimizar lucro, não um setpoint fixo')
    axs5[0].legend(); axs5[0].grid(True)

    axs5[1].plot(t5, lucro_acumulado, color='darkgreen', label='Lucro acumulado')
    axs5[1].set_title('Lucro Acumulado (receita pela conversão menos custo energético da jaqueta)')
    axs5[1].set_xlabel('Tempo (min)'); axs5[1].set_ylabel('$ (ilustrativo)')
    axs5[1].legend(); axs5[1].grid(True)
    fig5.tight_layout(); fig5.savefig('economic_mpc.png', dpi=150)

    plt.show()
