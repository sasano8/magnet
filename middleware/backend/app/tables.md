## case_node
| name | type | pk | unique | index | nullable | default | comment |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| id | INTEGER | x |  |  |  |  |  |
| name | VARCHAR(255) |  |  |  |  |  |  |
| is_system | BOOLEAN |  |  |  |  | False |  |
| description | VARCHAR(255) |  |  |  |  |  |  |

## target
| name | type | pk | unique | index | nullable | default | comment |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| id | INTEGER | x |  |  |  |  |  |
| name | VARCHAR(255) |  |  |  |  |  |  |
| node_id | INTEGER |  |  |  | x |  |  |

## users
| name | type | pk | unique | index | nullable | default | comment |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| id | INTEGER | x |  |  |  |  |  |
| username | VARCHAR |  | x | x | x |  |  |
| hashed_password | VARCHAR |  |  |  | x |  |  |
| email | VARCHAR |  | x | x | x |  |  |
| full_name | VARCHAR |  |  |  | x |  |  |
| disabled | BOOLEAN |  |  |  | x | False |  |
| is_active | BOOLEAN |  |  |  | x | True |  |
| is_test | BOOLEAN |  |  |  | x | True |  |

## items
| name | type | pk | unique | index | nullable | default | comment |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| id | INTEGER | x |  |  |  |  |  |
| title | VARCHAR |  |  | x | x |  |  |
| description | VARCHAR |  |  | x | x |  |  |
| owner_id | INTEGER |  |  |  | x |  |  |

## keywords
| name | type | pk | unique | index | nullable | default | comment |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| id | INTEGER | x |  |  |  |  |  |
| category_name | VARCHAR |  | x | x | x |  |  |
| tag | VARCHAR |  |  | x | x |  |  |
| max_size | INTEGER |  |  |  | x |  |  |

## executor
| name | type | pk | unique | index | nullable | default | comment |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| id | INTEGER | x |  |  |  |  |  |
| is_system | BOOLEAN |  |  |  |  | False |  |
| name | VARCHAR |  |  |  | x | "" |  |
| description | VARCHAR |  |  |  |  | "" |  |
| executor_name | VARCHAR |  |  |  |  | "" |  |
| pipeline_name | VARCHAR |  |  |  |  | "" |  |

## executor_job
| name | type | pk | unique | index | nullable | default | comment |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| id | INTEGER | x |  |  |  |  |  |
| pipeline | VARCHAR(255) |  |  |  | x |  |  |
| crawler_name | VARCHAR(255) |  |  |  | x |  |  |
| keyword | VARCHAR(255) |  |  |  | x |  |  |
| option_keywords | JSON |  |  |  |  | [] |  |
| deps | INTEGER |  |  |  |  | -1 |  |

## __crypto_ohlc_daily
外部データソースから取得したチャート

| name | type | pk | unique | index | nullable | default | comment |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| id | INTEGER | x |  |  |  |  |  |
| provider | VARCHAR(255) |  |  |  |  | "" |  |
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
| t_sma_5 | FLOAT |  |  |  |  | 0 |  |
| t_sma_10 | FLOAT |  |  |  |  | 0 |  |
| t_sma_15 | FLOAT |  |  |  |  | 0 |  |
| t_sma_20 | FLOAT |  |  |  |  | 0 |  |
| t_sma_25 | FLOAT |  |  |  |  | 0 |  |
| t_sma_30 | FLOAT |  |  |  |  | 0 |  |
| t_sma_200 | FLOAT |  |  |  |  | 0 |  |
| t_cross | INTEGER |  |  |  |  | 0 | 1=golden cross -1=dead cross |

## __topic
| name | type | pk | unique | index | nullable | default | comment |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| id | INTEGER | x |  |  |  |  |  |
| referer | VARCHAR(1023) |  |  |  | x |  |  |
| url | VARCHAR(1023) |  |  |  | x |  |  |
| url_cache | VARCHAR(1023) |  |  |  | x |  |  |
| title | VARCHAR(1023) |  |  |  | x | "" |  |
| summary | VARCHAR(1023) |  |  |  | x | "" |  |
| memo | VARCHAR(1023) |  |  |  |  | "" |  |
| detail | JSON |  |  |  |  | {} |  |

## trade_profile
| name | type | pk | unique | index | nullable | default | comment |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| id | INTEGER | x |  |  |  |  |  |
| name | VARCHAR(255) |  |  |  |  |  |  |
| description | VARCHAR(1024) |  |  |  |  |  |  |
| provider | VARCHAR(255) |  |  |  |  |  |  |
| market | VARCHAR(255) |  |  |  |  |  |  |
| product | VARCHAR(255) |  |  |  |  |  |  |
| periods | INTEGER |  |  |  |  |  |  |
| cron | VARCHAR(255) |  |  |  |  |  |  |
| broker | VARCHAR(255) |  |  |  |  |  |  |
| order_id | FLOAT |  |  |  | x |  |  |
| trade_rule | JSON |  |  |  |  | {} |  |

## trade_job
| name | type | pk | unique | index | nullable | default | comment |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| id | INTEGER | x |  |  |  |  |  |
| name | VARCHAR(255) |  |  |  |  |  |  |
| description | VARCHAR(1024) |  |  |  |  |  |  |
| provider | VARCHAR(255) |  |  |  |  |  |  |
| market | VARCHAR(255) |  |  |  |  |  |  |
| product | VARCHAR(255) |  |  |  |  |  |  |
| periods | INTEGER |  |  |  |  |  |  |
| cron | VARCHAR(255) |  |  |  |  |  |  |
| broker | VARCHAR(255) |  |  |  |  |  |  |
| order_id | FLOAT |  |  |  | x |  |  |
| trade_rule | JSON |  |  |  |  | {} |  |

## ingester_jobgroup
| name | type | pk | unique | index | nullable | default | comment |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| id | INTEGER | x |  |  |  |  |  |
| is_system | BOOLEAN |  |  |  |  | False |  |
| description | VARCHAR(1023) |  |  |  |  | "" |  |
| target_id | INTEGER |  |  |  | x |  |  |

## ingester_job
| name | type | pk | unique | index | nullable | default | comment |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| id | INTEGER | x |  |  |  |  |  |
| parent_id | INTEGER |  |  |  | x |  |  |
| description | VARCHAR(1023) |  |  |  |  | "" |  |
| pipeline_name | VARCHAR(255) |  |  |  | x |  |  |
| crawler_name | VARCHAR(255) |  |  |  | x |  |  |
| keyword | VARCHAR(255) |  |  |  | x |  |  |
| option_keywords | JSON |  |  |  |  | [] |  |
| deps | INTEGER |  |  |  |  | -1 |  |

## ingester
| name | type | pk | unique | index | nullable | default | comment |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| id | INTEGER | x |  |  |  |  |  |
| parent_id | INTEGER |  |  |  | x |  |  |
| pipeline_name | VARCHAR(255) |  |  |  | x |  |  |
| crawler_name | VARCHAR(255) |  |  |  | x |  |  |
| keyword | VARCHAR(255) |  |  |  | x |  |  |
| option_keywords | JSON |  |  |  |  | [] |  |
| deps | INTEGER |  |  |  |  | -1 |  |
| referer | VARCHAR(1023) |  |  |  | x |  |  |
| url | VARCHAR(1023) |  |  |  | x |  |  |
| url_cache | VARCHAR(1023) |  |  |  | x |  |  |
| title | VARCHAR(1023) |  |  |  | x | "" |  |
| summary | VARCHAR(1023) |  |  |  | x | "" |  |
| current_page_num | INTEGER |  |  |  |  | -1 |  |
| detail | JSON |  |  |  |  | {} |  |
