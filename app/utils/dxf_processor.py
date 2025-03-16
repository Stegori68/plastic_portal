import ezdxf
import math

def process_dxf(file_path):
    doc = ezdxf.readfile(file_path)
    msp = doc.modelspace()
    
    entities = []
    for entity in msp:
        if entity.dxftype() in ['LINE', 'LWPOLYLINE', 'CIRCLE', 'ARC']:
            entities.append(entity)
    
    # Calcola bounding box
    min_x = min(entity.dxf.start.x for entity in entities if hasattr(entity, 'dxf') and hasattr(entity.dxf, 'start'))
    max_x = max(entity.dxf.end.x for entity in entities if hasattr(entity, 'dxf') and hasattr(entity.dxf, 'end'))
    min_y = min(entity.dxf.start.y for entity in entities if hasattr(entity, 'dxf') and hasattr(entity.dxf, 'start'))
    max_y = max(entity.dxf.end.y for entity in entities if hasattr(entity, 'dxf') and hasattr(entity.dxf, 'end'))
    
    return {
        'width': max_x - min_x,
        'height': max_y - min_y,
        'area': (max_x - min_x) * (max_y - min_y)
    }