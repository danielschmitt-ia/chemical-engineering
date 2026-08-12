import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from reator_digital_twin import ConfiguracaoReator, ReatorCSTR, carregar_config  # noqa: E402


@pytest.fixture
def config_padrao() -> ConfiguracaoReator:
    return carregar_config(RAIZ / "configs" / "reator_padrao.yaml")


@pytest.fixture
def config_industrial() -> ConfiguracaoReator:
    return carregar_config(RAIZ / "configs" / "exemplo_planta_industrial.yaml")


@pytest.fixture
def reator(config_padrao) -> ReatorCSTR:
    return ReatorCSTR(config_padrao)
