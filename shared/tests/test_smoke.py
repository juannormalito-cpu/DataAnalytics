def test_imports():
    from shared_core.config.settings import load_settings
    from shared_core.database.engine import get_engine
    from shared_core.etl.contracts import Extractor, Loader, Transformer
    from shared_core.io.csv import load_csv, save_csv
    from shared_core.logging.logger import setup_logger

    assert load_settings
    assert setup_logger
    assert get_engine
    assert load_csv and save_csv
    assert Extractor and Transformer and Loader
