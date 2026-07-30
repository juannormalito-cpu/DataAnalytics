def test_cli_imports():
    from src.application.use_cases.evaluate_project import evaluate
    from src.application.use_cases.ingest_series import build_catalog, run_ingestion
    from src.interfaces.cli import main

    assert main
    assert evaluate
    assert run_ingestion
    assert len(build_catalog()) == 10
