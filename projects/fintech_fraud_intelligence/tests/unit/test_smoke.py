def test_cli_imports():
    from src.application.use_cases.run_pipeline import run_pipeline
    from src.interfaces.cli import main

    assert main
    assert run_pipeline
