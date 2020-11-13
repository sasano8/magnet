import pytest
from magnet.trade_profile import schemas

@pytest.mark.parametrize("amount", [
        schemas.RuleAmount(mode="amount", value=-1),
        schemas.RuleAmount(mode="amount", value=-0.000001),
])
def test_amount_invalid(amount):
    entry = schemas.OrderLogic(amount=amount)

    with pytest.raises(ValueError, match="Specify a value of 0 and more."):
        schemas.RuleTrade(entry=entry)


@pytest.mark.parametrize("amount", [
    schemas.RuleAmount(mode="amount", value=0),
    schemas.RuleAmount(mode="amount", value=0.000001),
    schemas.RuleAmount(mode="amount", value=1),
    schemas.RuleAmount(mode="amount", value=1.000001),
])
def test_amount_valid(amount):
    entry = schemas.OrderLogic(amount=amount)
    obj = schemas.RuleTrade(entry=entry)


@pytest.mark.parametrize("amount", [
    schemas.RuleAmount(mode="rate", value=-1),
    schemas.RuleAmount(mode="rate", value=-0.000001),
    schemas.RuleAmount(mode="rate", value=1.000001),
    schemas.RuleAmount(mode="rate", value=2),
])
def test_amount_rate_invalid(amount):
    entry = schemas.OrderLogic(amount=amount)

    with pytest.raises(ValueError, match="Specify a value between 0 and 1."):
        schemas.RuleTrade(entry=entry)


@pytest.mark.parametrize("amount", [
    schemas.RuleAmount(mode="rate", value=0),
    schemas.RuleAmount(mode="rate", value=0.000001),
    schemas.RuleAmount(mode="rate", value=0.5),
    schemas.RuleAmount(mode="rate", value=0.999999),
    schemas.RuleAmount(mode="rate", value=1),
])
def test_amount_rate_valid(amount):
    entry = schemas.OrderLogic(amount=amount)
    obj = schemas.RuleTrade(entry=entry)
