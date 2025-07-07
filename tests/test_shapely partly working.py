from shapely.geometry import Polygon, Point
from shapely.affinity import rotate, translate
import math
import matplotlib.pyplot as plt
from shapely.geometry import mapping


class Sheet:
    def __init__(self, width, height):
        """Initialize a sheet with given dimensions."""
        self.width = width
        self.height = height
        self.shapes = []  # List of placed shapes

    def can_place(self, shape):
        """Check if the shape can be placed on the sheet or inside another shape without overlapping."""
        if not self.is_within_bounds(shape):
            return False

        for placed_shape in self.shapes:
            # Allow touching but prevent overlapping
            if shape.intersects(placed_shape) and not shape.touches(placed_shape):
                return False

        return True

    def is_within_bounds(self, shape):
        """Check if the shape is contained within the sheet boundaries."""
        sheet_boundary = Polygon([(0, 0), (self.width, 0), (self.width, self.height), (0, self.height)])
        return sheet_boundary.contains(shape)

    def place_shape(self, shape):
        """Place the shape on the sheet if possible."""
        if self.can_place(shape):
            self.shapes.append(shape)
            return True
        return False


def rotate_point(point, angle, origin=(0, 0)):
    """Ruota un punto attorno a un'origine specificata."""
    angle_rad = math.radians(angle)
    ox, oy = origin
    px, py = point
    qx = ox + math.cos(angle_rad) * (px - ox) - math.sin(angle_rad) * (py - oy)
    qy = oy + math.sin(angle_rad) * (px - ox) + math.cos(angle_rad) * (py - oy)
    return qx, qy


def generate_shape(shape_type, size1, size2=None, opening_angle=90):
    """
    Generate a single shape based on the given type and dimensions.
    Supported types: rectangle, square, circle, arc.
    """
    if size1 <= 0 or (size2 is not None and size2 <= 0):
        raise ValueError("Dimensions must be greater than 0.")
        
    if shape_type == "rectangle":
        points = [(0, 0), (size1, 0), (size1, size2), (0, size2)]
        return Polygon(points)

    elif shape_type == "square":
        points = [(0, 0), (size1, 0), (size1, size1), (0, size1)]
        return Polygon(points)

    elif shape_type == "circle":
        num_points = 30  # Higher number for smoother circle
        points = [
            (math.cos(2 * math.pi / num_points * i) * size1,
             math.sin(2 * math.pi / num_points * i) * size1)
            for i in range(num_points)
        ]
        return Polygon(points)

    elif shape_type == "arc":
        if size2 is None:
            raise ValueError("Arc requires two dimensions (inner and outer radii).")
        if opening_angle <= 0 or opening_angle > 360:
            raise ValueError("Opening angle must be between 0 and 360 degrees for arcs.")
        
        # Generate the outer arc points
        outer_arc = [
            (math.cos(math.radians(angle)) * size2, math.sin(math.radians(angle)) * size2)
            for angle in range(0, opening_angle + 1, 5)  # Step of 5 degrees for smoothness
        ]
        
        # Generate the inner arc points (reversed)
        inner_arc = [
            (math.cos(math.radians(angle)) * size1, math.sin(math.radians(angle)) * size1)
            for angle in range(opening_angle, -1, -5)
        ]
        
        # Combine the points to form a closed shape
        points = outer_arc + inner_arc
        
        # Apply rotation if needed
        
        return Polygon(points)

    else:
        raise ValueError(f"Unsupported shape type: {shape_type}")


def fill_sheet_with_shape(sheet, shape):
    """
    Fill the sheet with as many instances of the given shape as possible.
    Use hexagonal packing for circular shapes and rectangular packing for others.
    """
    if isinstance(shape, Polygon) and len(shape.exterior.coords) > 20:  # Assume circular shape
        # Hexagonal packing for circular shapes
        best_layout = []
        best_waste = float('inf')

        # Get the diameter of the circle
        diameter = shape.bounds[2] - shape.bounds[0]

        # Hexagonal packing parameters
        row_height = diameter * math.sqrt(3) / 2  # Vertical distance between rows
        col_width = diameter  # Horizontal distance between columns

        for rotation_angle in range(0, 360, 15):  # Optional: Try different rotations
            rotated_shape = rotate(shape, rotation_angle, origin='center', use_radians=False)

            # Temporary layout for this rotation
            current_layout = []
            for row in range(int(sheet.height // row_height)):
                for col in range(int(sheet.width // col_width)):
                    # Offset every other row for hexagonal packing
                    x_offset = col * col_width
                    y_offset = row * row_height
                    if row % 2 == 1:
                        x_offset += col_width / 2

                    translated_shape = translate(rotated_shape, xoff=x_offset, yoff=y_offset)
                    if sheet.can_place(translated_shape):
                        sheet.place_shape(translated_shape)
                        current_layout.append(translated_shape)

            # Calculate waste (unused area)
            used_area = sum(s.area for s in current_layout)
            total_area = sheet.width * sheet.height
            waste = total_area - used_area

            # Keep the best layout
            if waste < best_waste:
                best_waste = waste
                best_layout = current_layout

            # Reset the sheet for the next rotation
            sheet.shapes = []

        # Apply the best layout
        sheet.shapes = best_layout

    else:
        # Rectangular packing for other shapes
        best_layout = []
        best_waste = float('inf')

        # Try different rotations and placements
        for rotation_angle in range(0, 360, 15):  # Rotate in steps of 15°
            rotated_shape = rotate(shape, rotation_angle, origin='center', use_radians=False)

            # Get the dimensions of the rotated shape
            rotated_width = rotated_shape.bounds[2] - rotated_shape.bounds[0]
            rotated_height = rotated_shape.bounds[3] - rotated_shape.bounds[1]

            # Temporary layout for this rotation
            current_layout = []
            for x_offset in range(0, int(sheet.width), int(rotated_width)):
                for y_offset in range(0, int(sheet.height), int(rotated_height)):
                    translated_shape = translate(rotated_shape, xoff=x_offset, yoff=y_offset)
                    if sheet.can_place(translated_shape):
                        sheet.place_shape(translated_shape)
                        current_layout.append(translated_shape)

            # Calculate waste (unused area)
            used_area = sum(s.area for s in current_layout)
            total_area = sheet.width * sheet.height
            waste = total_area - used_area

            # Keep the best layout
            if waste < best_waste:
                best_waste = waste
                best_layout = current_layout

            # Reset the sheet for the next rotation
            sheet.shapes = []

        # Apply the best layout
        sheet.shapes = best_layout


def plot_sheet(sheet):
    fig, ax = plt.subplots()
    ax.set_xlim(0, sheet.width)
    ax.set_ylim(0, sheet.height)
    for shape in sheet.shapes:
        if shape.is_empty or not shape.is_valid:
            continue
        x, y = shape.exterior.xy
        ax.fill(x, y, alpha=0.5, edgecolor='black', linewidth=1)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()


def main():
    # Define sheet dimensions
    sheet_width = 294.8
    sheet_height = 294.8
    sheet = Sheet(sheet_width, sheet_height)

    # Define the shape type and dimensions
    shape_type = "circle"  # Options: rectangle, square, circle, arc
    size1 = 120  # For rectangle, square, or circle, this is the width/diameter. For arc, this is the inner radius.
    size2 = 101  # Optional for arc (outer radius) or rectangle (height).
    opening_angle = 90  # Set a valid opening angle for the arc (e.g., 180 degrees).

    # Generate the shapes
    shape = generate_shape(shape_type, size1, size2, opening_angle)

    # Fill the sheet with the shape
    fill_sheet_with_shape(sheet, shape)

    # Plot the sheet with the placed shapes
    plot_sheet(sheet)

    # Save the sheet and shapes to a file (optional)
    with open("sheet_shapes.txt", "w") as file:
        file.write(f"Sheet dimensions: {sheet.width} x {sheet.height}\n")
        file.write(f"Number of shapes placed: {len(sheet.shapes)}\n\n")
        for i, placed_shape in enumerate(sheet.shapes, 1):
            file.write(f"Shape {i}: {mapping(placed_shape)}\n")


if __name__ == '__main__':
    main()