import math

class CostCalculator:
    def calculate_costs(self):
        # Calcolo elementi per lastra
        elements_per_sheet = self._calculate_elements_per_sheet()
        
        # Calcolo per plotter
        plotter = ProductionType.query.filter_by(category="plotter").first()
        plotter_cost = self._calculate_plotter_cost(plotter, elements_per_sheet)
        
        # Calcolo per fustella
        fustella = ProductionType.query.filter_by(category="fustella").first()
        fustella_cost = self._calculate_fustella_cost(fustella, elements_per_sheet)
        
        # Trova punto di break-even
        break_even = self._find_break_even_point(
            plotter_cost, 
            fustella_cost, 
            elements_per_sheet
        )
        
        return {
            'plotter': plotter_cost,
            'fustella': fustella_cost,
            'break_even': break_even
        }

    def _calculate_plotter_cost(self, production_type, elements_per_sheet):
        sheets_needed = math.ceil(self.quantity / elements_per_sheet)
        total_cost = (
            production_type.setup_cost + 
            (production_type.cutting_cost * sheets_needed)
        )
        return {
            'unit_cost': total_cost / self.quantity,
            'total_cost': total_cost,
            'sheets': sheets_needed
        }

    def _calculate_fustella_cost(self, production_type, elements_per_sheet):
        sheets_needed = math.ceil(self.quantity / elements_per_sheet)
        total_cost = (
            production_type.tooling_cost +
            production_type.setup_cost + 
            (production_type.cutting_cost * sheets_needed)
        )
        return {
            'unit_cost': total_cost / self.quantity,
            'total_cost': total_cost,
            'sheets': sheets_needed
        }

    def _find_break_even_point(self, plotter, fustella, elements_per_sheet):
        try:
            # Formula per calcolo teorico
            delta_setup = fustella['total_cost'] - plotter['total_cost']
            delta_per_unit = plotter['unit_cost'] - fustella['unit_cost']
            
            if delta_per_unit <= 0:
                return None
                
            break_even = math.ceil(abs(delta_setup / delta_per_unit))
            
            # Verifica effettiva
            for q in range(max(1, break_even-10), break_even+10):
                plotter_q = self._calculate_plotter_cost(q, elements_per_sheet)
                fustella_q = self._calculate_fustella_cost(q, elements_per_sheet)
                
                if fustella_q['unit_cost'] < plotter_q['unit_cost']:
                    return q
            return break_even
        except:
            return None