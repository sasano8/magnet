from magnet.database import get_db

def clear_all_session():
    db = get_db().__iter__().__next__()
    sql = "select * from pg_stat_activity"
    result = db.execute(sql)

    # select pg_terminate_backend(pid) from pg_stat_activity


