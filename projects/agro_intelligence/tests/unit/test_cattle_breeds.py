from src.application.use_cases.cattle_breeds import CATTLE_BREEDS, recommended_breeds_for


def test_all_breeds_have_required_fields():
    for breed in CATTLE_BREEDS:
        assert breed.name
        assert breed.recommended_provinces
        assert breed.source


def test_recommended_breeds_for_corrientes_favors_tick_resistant_crosses():
    breeds = recommended_breeds_for("Corrientes")
    names = {breed.name for breed in breeds}

    assert "Braford" in names
    assert "Brangus" in names
    assert "Angus" not in names  # baja resistencia a garrapata, no recomendada en el NEA


def test_recommended_breeds_for_buenos_aires_favors_british_breeds():
    breeds = recommended_breeds_for("Buenos Aires")
    names = {breed.name for breed in breeds}

    assert "Angus" in names
    assert "Hereford" in names


def test_recommended_breeds_for_unknown_province_is_empty():
    assert recommended_breeds_for("Neverland") == []
