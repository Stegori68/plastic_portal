import svgnest

def calculate_nesting(file_path, sheet_dimensions):
    nest = svgnest.Nest()
    sheet = svgnest.Sheet(sheet_dimensions[0], sheet_dimensions[1])
    parts = svgnest.load_dxf(file_path)  # Conversione da DXF a SVG se necessario
    
    nest.fit(parts, [sheet])
    return {
        'sheets_used': len(nest.sheets),
        'efficiency': nest.efficiency()
    }