import pytest

from planta_biodiesel.fluxograma import (
    ParametrosPlantaBiodiesel,
    avaliar_financeiro,
    avaliar_seguranca,
    avaliar_sustentabilidade,
    dimensionar_agitacao,
    dimensionar_transferencia,
    economia_atomica_transesterificacao,
    massa_molar_fame,
    simular_decantacao,
    simular_integracao_termica,
    simular_lavagem,
    simular_planta,
    simular_reator,
    simular_recuperacao_metanol,
)


@pytest.fixture
def params():
    return ParametrosPlantaBiodiesel()


class TestReator:
    def test_balanco_de_massa_fecha_exatamente(self, params):
        r = simular_reator(params)
        assert r.massa_saida_g_min == pytest.approx(r.massa_entrada_g_min, rel=1e-9)

    def test_massa_molar_fame_fecha_estequiometria(self, params):
        M_fame = massa_molar_fame(params)
        # TG + 3 MeOH -> 3 FAME + Glicerol: massa se conserva na propria reacao
        assert (params.massa_molar_trigliceridio + 3 * params.massa_molar_metanol) == pytest.approx(
            3 * M_fame + params.massa_molar_glicerol, rel=1e-9)

    def test_conversao_maior_produz_mais_fame(self, params):
        baixa = simular_reator(ParametrosPlantaBiodiesel(conversao_projeto=0.80))
        alta = simular_reator(ParametrosPlantaBiodiesel(conversao_projeto=0.98))
        assert alta.fame_mol_min > baixa.fame_mol_min
        assert alta.trigliceridio_mol_min < baixa.trigliceridio_mol_min


class TestDecantacao:
    def test_componentes_se_conservam_entre_as_duas_fases(self, params):
        reator = simular_reator(params)
        dec = simular_decantacao(reator, params)
        for componente, total in [("FAME", reator.fame_mol_min), ("Glicerol", reator.glicerol_mol_min),
                                   ("MeOH", reator.metanol_mol_min), ("TG", reator.trigliceridio_mol_min)]:
            soma = dec.fase_leve_mol_min[componente] + dec.fase_pesada_mol_min[componente]
            assert soma == pytest.approx(total, rel=1e-9)

    def test_fase_leve_e_predominantemente_fame(self, params):
        reator = simular_reator(params)
        dec = simular_decantacao(reator, params)
        assert dec.fase_leve_mol_min["FAME"] > dec.fase_pesada_mol_min["FAME"]

    def test_fase_pesada_e_predominantemente_glicerol(self, params):
        reator = simular_reator(params)
        dec = simular_decantacao(reator, params)
        assert dec.fase_pesada_mol_min["Glicerol"] > dec.fase_leve_mol_min["Glicerol"]

    def test_area_decantador_positiva(self, params):
        reator = simular_reator(params)
        dec = simular_decantacao(reator, params)
        assert dec.area_decantador_m2 > 0
        assert dec.velocidade_sedimentacao_m_s < dec.velocidade_stokes_m_s  # dificultada < Stokes puro


class TestLavagem:
    def test_mais_estagios_removem_mais_glicerol(self, params):
        reator = simular_reator(params)
        dec = simular_decantacao(reator, params)
        lav = simular_lavagem(dec, params)
        assert lav.estagios_recomendados >= 1
        assert lav.remocao_um_estagio < params.remocao_alvo_lavagem

    def test_maior_coeficiente_distribuicao_exige_menos_estagios(self, params):
        # Mantem o fator de extracao E=m*(S/F) > 1 nos dois casos -- com E<1 a remocao maxima
        # assintotica (N->infinito) e limitada a (1-E), tornando a meta de 95% inatingivel e
        # numero_estagios_kremser corretamente levanta erro (log de numero negativo).
        reator = simular_reator(params)
        dec = simular_decantacao(reator, params)
        lav_baixo_m = simular_lavagem(dec, ParametrosPlantaBiodiesel(coeficiente_distribuicao_glicerol=10.0))
        lav_alto_m = simular_lavagem(dec, ParametrosPlantaBiodiesel(coeficiente_distribuicao_glicerol=50.0))
        assert lav_alto_m.estagios_para_meta < lav_baixo_m.estagios_para_meta


class TestRecuperacaoMetanol:
    def test_biodiesel_final_e_alimentacao_menos_vapor(self, params):
        reator = simular_reator(params)
        dec = simular_decantacao(reator, params)
        rec = simular_recuperacao_metanol(dec, params)
        assert rec.biodiesel_final_kg_min == pytest.approx(rec.alimentacao_kg_min - rec.vapor_metanol_kg_min)

    def test_pureza_final_bate_com_alvo(self, params):
        reator = simular_reator(params)
        dec = simular_decantacao(reator, params)
        rec = simular_recuperacao_metanol(dec, params)
        assert rec.pureza_final == pytest.approx(params.pureza_fame_alvo, rel=1e-6)


class TestIntegracaoTermica:
    def test_balanco_de_energia_da_cascata_fecha(self, params):
        reator = simular_reator(params)
        dec = simular_decantacao(reator, params)
        lav = simular_lavagem(dec, params)
        rec = simular_recuperacao_metanol(dec, params)
        pinch = simular_integracao_termica(reator, lav, rec, params)

        t = params.temperaturas_correntes
        duty_quente_total = (
            (reator.massa_saida_g_min / 1000.0 / 60.0) * params.cp_organicos * abs(t["produto_reator"][0] - t["produto_reator"][1])
            + (rec.vapor_metanol_kg_min / 60.0) * params.cp_vapor_metanol * abs(t["vapor_metanol"][0] - t["vapor_metanol"][1])
        )
        duty_fria_total = (
            (params.vazao_molar_trigliceridio * params.massa_molar_trigliceridio / 1000.0 / 60.0) * params.cp_organicos
            * abs(t["oleo_fresco"][1] - t["oleo_fresco"][0])
            + (lav.massa_agua_kg_min / 60.0) * params.cp_agua * abs(t["agua_lavagem"][1] - t["agua_lavagem"][0])
        )
        # utilidade_quente + duty das quentes == duty das frias + utilidade_fria (1a lei)
        assert pinch["utilidade_quente_minima"] + duty_quente_total == pytest.approx(
            duty_fria_total + pinch["utilidade_fria_minima"], rel=1e-6)

    def test_utilidades_nao_negativas(self, params):
        reator = simular_reator(params)
        dec = simular_decantacao(reator, params)
        lav = simular_lavagem(dec, params)
        rec = simular_recuperacao_metanol(dec, params)
        pinch = simular_integracao_termica(reator, lav, rec, params)
        assert pinch["utilidade_quente_minima"] >= 0
        assert pinch["utilidade_fria_minima"] >= 0


class TestTransferenciaEAgitacao:
    def test_dimensionamento_transferencia_positivo(self, params):
        reator = simular_reator(params)
        dec = simular_decantacao(reator, params)
        resultado = dimensionar_transferencia(dec, params)
        assert resultado["delta_p_total"] > 0
        assert resultado["espessura_parede_m"] > 0
        assert resultado["potencia_eixo_bomba_W"] > resultado["potencia_hidraulica_W"]  # eficiencia < 1

    def test_agitacao_positiva(self, params):
        resultado = dimensionar_agitacao(params)
        assert resultado["reynolds_agitacao"] > 0
        assert resultado["potencia_W"] > 0


class TestSeguranca:
    def test_tres_modos_de_falha_com_rpn_positivo(self):
        fmea = avaliar_seguranca()
        assert len(fmea) == 3
        assert all(item["rpn"] > 0 for item in fmea)


class TestFinanceiro:
    def test_preco_maior_aumenta_lucro(self, params):
        reator = simular_reator(params)
        dec = simular_decantacao(reator, params)
        rec = simular_recuperacao_metanol(dec, params)
        baixo = avaliar_financeiro(dec, rec, ParametrosPlantaBiodiesel(preco_biodiesel_kg=1.00))
        alto = avaliar_financeiro(dec, rec, ParametrosPlantaBiodiesel(preco_biodiesel_kg=1.50))
        assert alto.lucro_dia > baixo.lucro_dia
        assert alto.vpl > baixo.vpl

    def test_custo_oleo_maior_reduz_lucro(self, params):
        reator = simular_reator(params)
        dec = simular_decantacao(reator, params)
        rec = simular_recuperacao_metanol(dec, params)
        barato = avaliar_financeiro(dec, rec, ParametrosPlantaBiodiesel(preco_oleo_kg=0.80))
        caro = avaliar_financeiro(dec, rec, ParametrosPlantaBiodiesel(preco_oleo_kg=1.20))
        assert caro.lucro_dia < barato.lucro_dia

    def test_consumo_de_oleo_vem_da_alimentacao_nao_do_residual(self, params):
        # Regressao: consumo de materia-prima usava o residual nao-reagido (~5% da alimentacao)
        # em vez da alimentacao completa, subestimando o custo em ~20x.
        reator = simular_reator(params)
        dec = simular_decantacao(reator, params)
        rec = simular_recuperacao_metanol(dec, params)
        fin = avaliar_financeiro(dec, rec, params)
        custo_oleo_esperado = params.vazao_molar_trigliceridio * params.massa_molar_trigliceridio / 1000.0 * 60 * 24 * params.preco_oleo_kg
        assert fin.custo_materia_prima_dia > 0.9 * custo_oleo_esperado


class TestSustentabilidade:
    def test_co2_evitado_positivo_e_escala_com_producao(self):
        # Resimula a cadeia inteira para cada tamanho de planta -- passar vazao_molar_trigliceridio
        # so para avaliar_financeiro não muda a produção, que vem de `rec`/`dec` (calculados a
        # partir do reator real, não do parametro isolado).
        pequena = simular_planta(ParametrosPlantaBiodiesel(vazao_molar_trigliceridio=30.0))
        grande = simular_planta(ParametrosPlantaBiodiesel(vazao_molar_trigliceridio=100.0))
        assert pequena.sustentabilidade["co2_fossil_evitado_kg_dia"] > 0
        assert grande.sustentabilidade["co2_fossil_evitado_kg_dia"] > pequena.sustentabilidade["co2_fossil_evitado_kg_dia"]


class TestEconomiaAtomica:
    def test_proxima_de_90_por_cento(self, params):
        ae = economia_atomica_transesterificacao(params)
        assert 0.85 < ae < 0.95


class TestSimularPlantaEndToEnd:
    def test_roda_sem_erro_com_parametros_padrao(self):
        resultado = simular_planta()
        assert resultado.reator.fame_mol_min > 0
        assert resultado.financeiro.producao_fame_kg_dia > 0
        assert 0 < resultado.economia_atomica < 1

    def test_aceita_parametros_customizados(self):
        params = ParametrosPlantaBiodiesel(vazao_molar_trigliceridio=100.0, conversao_projeto=0.90)
        resultado = simular_planta(params)
        assert resultado.reator.fame_mol_min == pytest.approx(3 * 100.0 * 0.90)
