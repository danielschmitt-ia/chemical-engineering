"""Demonstra o fluxograma completo da planta de biodiesel (`planta_biodiesel/fluxograma.py`) —
do óleo alimentado ao reator até o biodiesel e a glicerina prontos para venda, passando por
decantação, lavagem, recuperação de metanol, integração térmica, dimensionamento de utilidades,
segurança, economia e sustentabilidade. Ver o módulo para a descrição de cada estágio e quais
funções de `calculos_processo/` cada um usa.

Uso:
    python demo_planta_biodiesel.py
"""

import matplotlib.pyplot as plt

from planta_biodiesel import ParametrosPlantaBiodiesel, simular_planta

if __name__ == "__main__":
    print("🏭 Simulando planta de biodiesel completa (reator → produto acabado)...")
    params = ParametrosPlantaBiodiesel()
    r = simular_planta(params)

    print("\n=== 1. Reator (transesterificação) ===")
    print(f"   Conversão de projeto: {params.conversao_projeto*100:.0f}%")
    print(f"   FAME produzido: {r.reator.fame_mol_min:.1f} mol/min | Glicerol: {r.reator.glicerol_mol_min:.1f} mol/min")
    print(f"   Balanço de massa do reator fecha com resíduo de "
          f"{abs(r.reator.massa_saida_g_min - r.reator.massa_entrada_g_min):.2e} g/min (essencialmente zero)")

    print("\n=== 2. Decantação gravitacional ===")
    print(f"   Área mínima do decantador: {r.decantacao.area_decantador_m2:.2f} m²")
    print(f"   Velocidade de sedimentação (Richardson-Zaki): {r.decantacao.velocidade_sedimentacao_m_s*1000:.3f} mm/s "
          f"({r.decantacao.velocidade_sedimentacao_m_s/r.decantacao.velocidade_stokes_m_s*100:.0f}% da velocidade de Stokes isolada)")

    print("\n=== 3. Lavagem com água (extração líquido-líquido) ===")
    print(f"   1 estágio remove {r.lavagem.remocao_um_estagio*100:.0f}% do glicerol residual")
    print(f"   Estágios recomendados para ≥95% de remoção: {r.lavagem.estagios_recomendados}")

    print("\n=== 4. Recuperação de metanol (evaporação) ===")
    print(f"   Metanol recuperado: {r.recuperacao_metanol.vapor_metanol_kg_min:.2f} kg/min "
          f"(reciclado à alimentação do reator)")
    print(f"   Biodiesel final: {r.recuperacao_metanol.biodiesel_final_kg_min:.1f} kg/min "
          f"a {r.recuperacao_metanol.pureza_final*100:.1f}% de pureza")

    print("\n=== 5. Integração térmica (pinch) ===")
    print(f"   Utilidade quente mínima: {r.pinch['utilidade_quente_minima']:.1f} kW")
    print(f"   Utilidade fria mínima: {r.pinch['utilidade_fria_minima']:.1f} kW")
    print(f"   Temperatura de pinch: {r.pinch['temperatura_pinch_quente']:.0f}°C (lado quente) / "
          f"{r.pinch['temperatura_pinch_fria']:.0f}°C (lado frio)")

    print("\n=== 6-7. Tubulação, bombeamento e agitação ===")
    print(f"   Perda de carga na linha reator→decantador: {r.transferencia['delta_p_total']/1000:.2f} kPa")
    print(f"   Potência de eixo da bomba: {r.transferencia['potencia_eixo_bomba_W']:.0f} W")
    print(f"   Potência do agitador da lavagem: {r.agitacao['potencia_W']:.0f} W")

    print("\n=== 8. Segurança (FMEA) ===")
    for item in sorted(r.seguranca, key=lambda x: -x["rpn"]):
        print(f"   RPN={item['rpn']:>3.0f}  {item['modo_falha']}")

    print("\n=== 9. Economia ===")
    print(f"   Produção: {r.financeiro.producao_fame_kg_dia:,.0f} kg/dia biodiesel + "
          f"{r.financeiro.producao_glicerina_kg_dia:,.0f} kg/dia glicerina bruta")
    print(f"   Margem sobre receita: {r.financeiro.margem*100:.1f}%")
    print(f"   Payback simples: {r.financeiro.payback_anos:.1f} anos")
    tir_str = f"{r.financeiro.tir*100:.1f}%" if r.financeiro.tir is not None else "não definida"
    print(f"   VPL ({params.taxa_desconto*100:.0f}% a.a., {params.vida_util_anos} anos): "
          f"${r.financeiro.vpl:,.0f} | TIR: {tir_str}")
    if r.financeiro.vpl < 0:
        print("   ⚠️  VPL negativo: nos preços ilustrativos usados, o projeto não cobre o custo de "
              "capital de 12% — reflete a margem historicamente apertada do biodiesel, sensível ao "
              "preço do óleo vegetal (a maior linha de custo) e a subsídios/mandatos de mistura.")

    print("\n=== 10. Sustentabilidade ===")
    print(f"   CO2 fóssil evitado (deslocando diesel): {r.sustentabilidade['co2_fossil_evitado_kg_dia']:,.0f} kg/dia")
    print(f"   Intensidade hídrica (lavagem): {r.sustentabilidade['intensidade_hidrica_m3_por_t']:.3f} m³ água/t biodiesel")

    print("\n=== 11. Economia atômica da transesterificação ===")
    print(f"   {r.economia_atomica*100:.1f}% (fração da massa dos reagentes que termina em produto vendável)")

    # ===== Figura resumo =====
    fig, axs = plt.subplots(2, 2, figsize=(12, 9))

    etapas = ["Alimentação\n(óleo+MeOH)", "Produto\nreator", "Fase leve\n(biodiesel bruto)", "Biodiesel\nfinal"]
    massas = [r.reator.massa_entrada_g_min / 1000.0, r.reator.massa_saida_g_min / 1000.0,
              r.lavagem.massa_fase_leve_kg_min, r.recuperacao_metanol.biodiesel_final_kg_min]
    axs[0, 0].bar(etapas, massas, color="darkgoldenrod")
    axs[0, 0].set_title("Vazão mássica ao longo do fluxograma")
    axs[0, 0].set_ylabel("kg/min")
    axs[0, 0].grid(True, axis="y")

    cascata = r.pinch["cascata_viavel"]
    axs[0, 1].plot(range(len(cascata)), cascata, marker="o", color="teal")
    idx_pinch = cascata.index(min(cascata))
    axs[0, 1].axvline(x=idx_pinch, color="red", linestyle="--", label="Ponto de pinch")
    axs[0, 1].set_title("Cascata de calor viável (Problem Table Algorithm)")
    axs[0, 1].set_xlabel("Fronteira de intervalo de temperatura")
    axs[0, 1].set_ylabel("Calor em cascata (kW)")
    axs[0, 1].legend(); axs[0, 1].grid(True)

    modos = [item["modo_falha"].split(" (")[0] for item in r.seguranca]
    rpns = [item["rpn"] for item in r.seguranca]
    cores = ["crimson" if rpn == max(rpns) else "steelblue" for rpn in rpns]
    axs[1, 0].barh(modos, rpns, color=cores)
    axs[1, 0].set_title("FMEA — Número de Prioridade de Risco (RPN)")
    axs[1, 0].set_xlabel("RPN (Severidade × Ocorrência × Detecção)")
    axs[1, 0].grid(True, axis="x")

    anos = list(range(params.vida_util_anos + 1))
    fluxo_acumulado = [-params.investimento_inicial]
    for _ in range(params.vida_util_anos):
        fluxo_acumulado.append(fluxo_acumulado[-1] + r.financeiro.fluxo_caixa_anual)
    axs[1, 1].plot(anos, fluxo_acumulado, marker="o", color="darkgreen")
    axs[1, 1].axhline(y=0, color="black", linestyle=":")
    axs[1, 1].axvline(x=r.financeiro.payback_anos, color="red", linestyle="--", label="Payback")
    axs[1, 1].set_title(f"Fluxo de caixa acumulado ({params.vida_util_anos} anos)")
    axs[1, 1].set_xlabel("Ano")
    axs[1, 1].set_ylabel("US$")
    axs[1, 1].legend(); axs[1, 1].grid(True)

    fig.tight_layout()
    fig.savefig("planta_biodiesel.png", dpi=150)
    print("\n📊 Figura salva em planta_biodiesel.png")
