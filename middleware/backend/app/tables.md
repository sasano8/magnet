## case_node
| name | type | pk | nullable | default | unique | index | comment |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| id | INTEGER | True |  |  |  |  |  |
| name | VARCHAR(255) |  |  |  |  |  |  |
| is_system | BOOLEAN |  |  | ColumnDefault(False) |  |  |  |
| description | VARCHAR(255) |  |  |  |  |  |  |

## target
| name | type | pk | nullable | default | unique | index | comment |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| id | INTEGER | True |  |  |  |  |  |
| name | VARCHAR(255) |  |  |  |  |  |  |
| node_id | INTEGER |  | True |  |  |  |  |

## users
| name | type | pk | nullable | default | unique | index | comment |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| id | INTEGER | True |  |  |  | True |  |
| username | VARCHAR |  | True |  | True | True |  |
| hashed_password | VARCHAR |  | True |  |  |  |  |
| email | VARCHAR |  | True |  | True | True |  |
| full_name | VARCHAR |  | True |  |  |  |  |
| disabled | BOOLEAN |  | True | ColumnDefault(False) |  |  |  |
| is_active | BOOLEAN |  | True | ColumnDefault(True) |  |  |  |
| is_test | BOOLEAN |  | True | ColumnDefault(True) |  |  |  |

## items
| name | type | pk | nullable | default | unique | index | comment |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| id | INTEGER | True |  |  |  | True |  |
| title | VARCHAR |  | True |  |  | True |  |
| description | VARCHAR |  | True |  |  | True |  |
| owner_id | INTEGER |  | True |  |  |  |  |

## keywords
| name | type | pk | nullable | default | unique | index | comment |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| id | INTEGER | True |  |  |  |  |  |
| category_name | VARCHAR |  | True |  | True | True |  |
| tag | VARCHAR |  | True |  |  | True |  |
| max_size | INTEGER |  | True |  |  |  |  |

## executor
| name | type | pk | nullable | default | unique | index | comment |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| id | INTEGER | True |  |  |  |  |  |
| is_system | BOOLEAN |  |  | ColumnDefault(False) |  |  |  |
| name | VARCHAR |  | True | ColumnDefault('') |  |  |  |
| description | VARCHAR |  |  | ColumnDefault('') |  |  |  |
| executor_name | VARCHAR |  |  | ColumnDefault('') |  |  |  |
| pipeline_name | VARCHAR |  |  | ColumnDefault('') |  |  |  |

## executor_job
| name | type | pk | nullable | default | unique | index | comment |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| id | INTEGER | True |  |  |  |  |  |
| pipeline | VARCHAR(255) |  | True |  |  |  |  |
| crawler_name | VARCHAR(255) |  | True |  |  |  |  |
| keyword | VARCHAR(255) |  | True |  |  |  |  |
| option_keywords | 多分JSON |  |  | ColumnDefault([]) |  |  |  |
| deps | INTEGER |  |  | ColumnDefault(-1) |  |  |  |

## __crypto_ohlc_daily
外部データソースから取得したチャート

| name | type | pk | nullable | default | unique | index | comment |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| id | INTEGER | True |  |  |  |  |  |
| provider | VARCHAR(255) |  |  | ColumnDefault('') |  |  |  |
| market | VARCHAR(255) |  |  |  |  |  |  |
| product | VARCHAR(255) |  |  |  |  |  |  |
| periods | INTEGER |  |  |  |  |  |  |
| close_time | DATETIME |  |  |  |  |  |  |
| open_price | FLOAT |  |  |  |  |  |  |
| high_price | FLOAT |  |  |  |  |  |  |
| low_price | FLOAT |  |  |  |  |  |  |
| close_price | FLOAT |  |  |  |  |  |  |
| volume | FLOAT |  |  |  |  |  |  |
| quote_volume | FLOAT |  |  |  |  |  |  |
| t_sma_5 | FLOAT |  |  | ColumnDefault(0) |  |  |  |
| t_sma_10 | FLOAT |  |  | ColumnDefault(0) |  |  |  |
| t_sma_15 | FLOAT |  |  | ColumnDefault(0) |  |  |  |
| t_sma_20 | FLOAT |  |  | ColumnDefault(0) |  |  |  |
| t_sma_25 | FLOAT |  |  | ColumnDefault(0) |  |  |  |
| t_sma_30 | FLOAT |  |  | ColumnDefault(0) |  |  |  |
| t_sma_200 | FLOAT |  |  | ColumnDefault(0) |  |  |  |
| t_cross | FLOAT |  |  | ColumnDefault(0) |  |  | 1=golden cross -1=dead cross |

## __topic
| name | type | pk | nullable | default | unique | index | comment |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| id | INTEGER | True |  |  |  |  |  |
| referer | VARCHAR(1023) |  | True |  |  |  |  |
| url | VARCHAR(1023) |  | True |  |  |  |  |
| url_cache | VARCHAR(1023) |  | True |  |  |  |  |
| title | VARCHAR(1023) |  | True | ColumnDefault('') |  |  |  |
| summary | VARCHAR(1023) |  | True | ColumnDefault('') |  |  |  |
| memo | VARCHAR(1023) |  |  | ColumnDefault('') |  |  |  |
| detail | 多分JSON |  |  | ColumnDefault({}) |  |  |  |

## trade_profile
| name | type | pk | nullable | default | unique | index | comment |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| id | INTEGER | True |  |  |  |  |  |
| name | VARCHAR(255) |  |  |  |  |  |  |
| description | VARCHAR(1024) |  |  |  |  |  |  |
| provider | VARCHAR(255) |  |  |  |  |  |  |
| market | VARCHAR(255) |  |  |  |  |  |  |
| product | VARCHAR(255) |  |  |  |  |  |  |
| periods | INTEGER |  |  |  |  |  |  |
| cron | VARCHAR(255) |  |  |  |  |  |  |
| broker | VARCHAR(255) |  |  |  |  |  |  |
| order_id | FLOAT |  | True |  |  |  |  |
| trade_rule | 多分JSON |  |  | ColumnDefault({}) |  |  |  |

## trade_job
| name | type | pk | nullable | default | unique | index | comment |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| id | INTEGER | True |  |  |  |  |  |
| name | VARCHAR(255) |  |  |  |  |  |  |
| description | VARCHAR(1024) |  |  |  |  |  |  |
| provider | VARCHAR(255) |  |  |  |  |  |  |
| market | VARCHAR(255) |  |  |  |  |  |  |
| product | VARCHAR(255) |  |  |  |  |  |  |
| periods | INTEGER |  |  |  |  |  |  |
| cron | VARCHAR(255) |  |  |  |  |  |  |
| broker | VARCHAR(255) |  |  |  |  |  |  |
| order_id | FLOAT |  | True |  |  |  |  |
| trade_rule | 多分JSON |  |  | ColumnDefault({}) |  |  |  |

## ingester_jobgroup
| name | type | pk | nullable | default | unique | index | comment |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| id | INTEGER | True |  |  |  | True |  |
| is_system | BOOLEAN |  |  | ColumnDefault(False) |  |  |  |
| description | VARCHAR(1023) |  |  | ColumnDefault('') |  |  |  |
| target_id | INTEGER |  | True |  |  |  |  |

## ingester_job
| name | type | pk | nullable | default | unique | index | comment |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| id | INTEGER | True |  |  |  | True |  |
| parent_id | INTEGER |  | True |  |  |  |  |
| description | VARCHAR(1023) |  |  | ColumnDefault('') |  |  |  |
| pipeline_name | VARCHAR(255) |  | True |  |  |  |  |
| crawler_name | VARCHAR(255) |  | True |  |  |  |  |
| keyword | VARCHAR(255) |  | True |  |  |  |  |
| option_keywords | 多分JSON |  |  | ColumnDefault([]) |  |  |  |
| deps | INTEGER |  |  | ColumnDefault(-1) |  |  |  |

## ingester
| name | type | pk | nullable | default | unique | index | comment |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| id | INTEGER | True |  |  |  | True |  |
| parent_id | INTEGER |  | True |  |  |  |  |
| pipeline_name | VARCHAR(255) |  | True |  |  |  |  |
| crawler_name | VARCHAR(255) |  | True |  |  |  |  |
| keyword | VARCHAR(255) |  | True |  |  |  |  |
| option_keywords | 多分JSON |  |  | ColumnDefault([]) |  |  |  |
| deps | INTEGER |  |  | ColumnDefault(-1) |  |  |  |
| referer | VARCHAR(1023) |  | True |  |  |  |  |
| url | VARCHAR(1023) |  | True |  |  |  |  |
| url_cache | VARCHAR(1023) |  | True |  |  |  |  |
| title | VARCHAR(1023) |  | True | ColumnDefault('') |  |  |  |
| summary | VARCHAR(1023) |  | True | ColumnDefault('') |  |  |  |
| current_page_num | INTEGER |  |  | ColumnDefault(-1) |  |  |  |
| detail | 多分JSON |  |  | ColumnDefault({}) |  |  |  |
