import pytest

from reator_digital_twin import ConfiguracaoReator, carregar_config


def test_valores_padrao_da_dataclass():
    cfg = ConfiguracaoReator()
    assert cfg.V == 100.0
    assert cfg.T_alvo == 330.0
    assert cfg.Tj_min < cfg.Tj_max


def test_carregar_config_padrao(config_padrao):
    assert config_padrao.nome_planta == "Reator CSTR (demonstração)"
    assert config_padrao.V == 100.0
    assert config_padrao.T_alvo == 330.0
    # notação científica sem sinal explícito no expoente (ex.: 7.2e+10) precisa virar float,
    # não string — é o formato usado no próprio arquivo de config.
    assert isinstance(config_padrao.Pre_exp_A, float)
    assert config_padrao.Pre_exp_A == pytest.approx(7.2e10)


def test_carregar_config_planta_industrial_e_distinta_da_padrao(config_padrao, config_industrial):
    assert config_industrial.nome_planta != config_padrao.nome_planta
    assert config_industrial.V != config_padrao.V
    assert config_industrial.tag_equipamento == "R-201"


def test_carregar_config_campo_desconhecido_falha(tmp_path):
    caminho = tmp_path / "invalido.yaml"
    caminho.write_text("campo_que_nao_existe: 123\n")
    with pytest.raises(ValueError, match="Campos desconhecidos"):
        carregar_config(caminho)


def test_carregar_config_valor_nao_numerico_falha(tmp_path):
    caminho = tmp_path / "invalido.yaml"
    caminho.write_text("V: not_a_number\n")
    with pytest.raises(ValueError):
        carregar_config(caminho)


def test_carregar_config_notacao_cientifica_sem_sinal_no_expoente(tmp_path):
    """Regressão: o PyYAML (SafeLoader) só reconhece notação científica como float quando o
    expoente tem sinal explícito (7.2e+10) — sem o sinal (7.2e10), o valor vira string. Este
    teste trava esse comportamento (carregar_config deve corrigir automaticamente)."""
    caminho = tmp_path / "sem_sinal.yaml"
    caminho.write_text("Pre_exp_A: 7.2e10\n")
    cfg = carregar_config(caminho)
    assert isinstance(cfg.Pre_exp_A, float)
    assert cfg.Pre_exp_A == pytest.approx(7.2e10)


def test_carregar_config_campos_omitidos_usam_padrao(tmp_path):
    caminho = tmp_path / "parcial.yaml"
    caminho.write_text("T_alvo: 400.0\n")
    cfg = carregar_config(caminho)
    assert cfg.T_alvo == 400.0
    assert cfg.V == ConfiguracaoReator().V  # não listado no YAML, mantém o padrão
