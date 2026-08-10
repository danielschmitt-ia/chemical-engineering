import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

class ReatorCSTR:
    def __init__(self):
        self.V = 100.0        # Volume do reator (L)
        self.F = 10.0         # Vazão volumétrica (L/min)
        self.CA0 = 2.0        # Concentração de entrada de A (mol/L)
        self.T0 = 300.0       # Temperatura de entrada (K)
        self.Pre_exp_A = 7.2e10 # Fator Arrhenius (1/min)
        self.Ea_R = 8750.0    # Ea/R (K)
        self.DeltaH = -50000.0 # Calor de reação (J/mol)
        self.rho = 1000.0     # Densidade (g/L)
        self.Cp = 4.184       # Cp (J/g·K)
        self.T_alvo = 330.0   # Setpoint do MPC (K)

    def calcular_cinetica(self, CA, T):
        k = self.Pre_exp_A * np.exp(-self.Ea_R / T)
        return k * CA

    def simular_runaway(self, UA_operacao, Tj=290.0, tempo_total=20, dt=0.02):
        passos = int(tempo_total / dt)
        CA, T = 2.0, 300.0
        hist_T = np.zeros(passos)
        hist_tempo = np.linspace(0, tempo_total, passos)
        
        for i in range(passos):
            hist_T[i] = T
            taxa = self.calcular_cinetica(CA, T)
            dCAdt = (self.F / self.V) * (self.CA0 - CA) - taxa
            dTdt = ((self.F / self.V) * (self.T0 - T)) + ((-self.DeltaH * taxa) / (self.rho * self.Cp)) + ((UA_operacao * (Tj - T)) / (self.V * self.rho * self.Cp))
            
            CA = max(0.0, CA + dCAdt * dt)
            T += dTdt * dt
            if T > 600:
                hist_T[i:] = T
                break
        return hist_tempo, hist_T

    def _prever_custo_mpc(self, acoes_Tj, CA_atual, T_atual, Hp, dt_mpc, UA):
        CA_pred, T_pred = CA_atual, T_atual
        custo = 0.0
        for Tj_predito in acoes_Tj:
            taxa = self.calcular_cinetica(CA_pred, T_pred)
            dCAdt = (self.F / self.V) * (self.CA0 - CA_pred) - taxa
            dTdt = ((self.F / self.V) * (self.T0 - T_pred)) + ((-self.DeltaH * taxa) / (self.rho * self.Cp)) + ((UA * (Tj_predito - T_pred)) / (self.V * self.rho * self.Cp))
            CA_pred = max(0.0, CA_pred + dCAdt * dt_mpc)
            T_pred += dTdt * dt_mpc
            custo += (T_pred - self.T_alvo) ** 2
        return custo

    def rodar_mpc(self, UA=50000.0, tempo_total=20, dt_mpc=0.25, Hp=5):
        passos = int(tempo_total / dt_mpc)
        hist_tempo = np.linspace(0, tempo_total, passos)
        hist_T, hist_Tj, hist_CA = np.zeros(passos), np.zeros(passos), np.zeros(passos)
        
        CA_real, T_real = 2.0, 300.0
        chute_Tj = [290.0] * Hp
        
        for i in range(passos):
            hist_T[i], hist_Tj[i], hist_CA[i] = T_real, chute_Tj[0], CA_real
            res = minimize(self._prever_custo_mpc, chute_Tj, args=(CA_real, T_real, Hp, dt_mpc, UA), bounds=[(240.0, 350.0)] * Hp, method='SLSQP')
            Tj_otimo = res.x[0]
            chute_Tj = list(res.x[1:]) + [res.x[-1]]
            
            taxa = self.calcular_cinetica(CA_real, T_real)
            dCAdt = (self.F / self.V) * (self.CA0 - CA_real) - taxa
            dTdt = ((self.F / self.V) * (self.T0 - T_real)) + ((-self.DeltaH * taxa) / (self.rho * self.Cp)) + ((UA * (Tj_otimo - T_real)) / (self.V * self.rho * self.Cp))
            CA_real = max(0.0, CA_real + dCAdt * dt_mpc)
            T_real += dTdt * dt_mpc
            
        return hist_tempo, hist_T, hist_Tj, hist_CA

if __name__ == "__main__":
    print("🚀 Executando simulação integrada...")
    reator = ReatorCSTR()
    t1, T_seguro = reator.simular_runaway(UA_operacao=50000.0)
    _, T_critico = reator.simular_runaway(UA_operacao=32000.0)
    t2, hist_T_mpc, hist_Tj_mpc, hist_CA_mpc = reator.rodar_mpc()
    
    X_dados = (hist_T_mpc + np.random.normal(0, 0.4, size=len(hist_T_mpc))).reshape(-1, 1)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_dados)
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, hist_CA_mpc, test_size=0.2, random_state=42)
    
    ia_sensor = MLPRegressor(hidden_layer_sizes=(15, 10), max_iter=2000, random_state=42)
    ia_sensor.fit(X_train, y_train)
    concentracao_predita = ia_sensor.predict(X_scaled)
    
    fig, axs = plt.subplots(3, 1, figsize=(10, 8))
    axs[0].plot(t1, T_seguro, label='Seguro')
    axs[0].plot(t1, T_critico, '--', label='Runaway')
    axs[0].legend(); axs[0].grid(True)
    axs[1].plot(t2, hist_T_mpc, color='purple')
    axs[1].axhline(y=330.0, color='black', linestyle=':')
    axs[1].grid(True)
    axs[2].plot(t2, hist_CA_mpc, label='Real')
    axs[2].plot(t2, concentracao_predita, '--', label='IA')
    axs[2].legend(); axs[2].grid(True)
    plt.tight_layout(); plt.show()
