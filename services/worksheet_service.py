from domain.structure import get_structure

def generate_worksheet(stage_id: str):
    structure = get_structure(stage_id)
    return structure["new_products"]
