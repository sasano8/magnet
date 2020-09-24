from enum import Enum

class CurrencyPair(Enum):
    btc_jpy = "btc_jpy"
    xem_jpy = 'xem_jpy'
    xem_btc = 'xem_btc'
    cszaif_zaif = "cszaif_zaif"
    csxem_xem = "csxem_xem"
    zaif_btc = "zaif_btc"
    mona_btc = "mona_btc"
    ncxc_btc = "ncxc_btc"
    cicc_btc = 'cicc_btc'
    eth_btc = 'eth_btc'
    xcp_btc = 'xcp_btc'
    ncxc_jpy = 'ncxc_jpy'
    zaif_jpy = 'zaif_jpy'
    erc20__cms_btc = 'erc20.cms_btc'
    cscmsxem_mosaic__cms = 'cscmsxem_mosaic.cms'
    fscc_btc = 'fscc_btc'
    mosaic__cms_jpy = 'mosaic.cms_jpy'
    xcp_jpy = 'xcp_jpy'
    cseth_eth = 'cseth_eth'
    cscmseth_erc20__cms = 'cscmseth_erc20.cms'
    mona_jpy = 'mona_jpy'
    eth_jpy = 'eth_jpy'
    erc20__cms_jpy = 'erc20.cms_jpy'
    bch_jpy = 'bch_jpy'
    csbtc_btc = 'csbtc_btc'
    jpyz_jpy = 'jpyz_jpy'
    cicc_jpy = 'cicc_jpy'
    bch_btc = 'bch_btc'
    fscc_jpy = 'fscc_jpy'
    mosaic__cms_btc = 'mosaic.cms_btc'

class Exchange(Enum):
    ZAIF = "zaif"
    BITFLYER = "bitflyer"