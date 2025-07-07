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
    Use rectangular packing with 0° and 90° rotations to maximize space utilization.
    """
    current_layout = []

    # Get the dimensions of the original shape
    shape_width = shape.bounds[2] - shape.bounds[0]
    shape_height = shape.bounds[3] - shape.bounds[1]

    # Phase 1: Fill with original orientation (0°)
    x_offset = 0
    y_offset = 0

    while y_offset + shape_height <= sheet.height:
        while x_offset + shape_width <= sheet.width:
            translated_shape = translate(shape, xoff=x_offset, yoff=y_offset)
            if sheet.can_place(translated_shape):
                sheet.place_shape(translated_shape)
                current_layout.append(translated_shape)
            x_offset += shape_width
        x_offset = 0  # Reset x_offset for the next row
        y_offset += shape_height

    # Phase 2: Fill remaining space with rotated shapes (90°)
    rotated_shape = rotate(shape, 90, origin='center', use_radians=False)
    rotated_width = rotated_shape.bounds[2] - rotated_shape.bounds[0]
    rotated_height = rotated_shape.bounds[3] - rotated_shape.bounds[1]

    # Find the starting position for rotated shapes
    x_offset = max([s.bounds[2] for s in current_layout]) if current_layout else 0
    y_offset = 0

    while x_offset + rotated_width <= sheet.width:
        while y_offset + rotated_height <= sheet.height:
            translated_shape = translate(rotated_shape, xoff=x_offset, yoff=y_offset)
            if sheet.can_place(translated_shape):
                sheet.place_shape(translated_shape)
                current_layout.append(translated_shape)
            y_offset += rotated_height
        if y_offset + rotated_height > sheet.height:
            break  # Exit if no more space vertically
        y_offset = 0  # Reset y_offset for the next column
        x_offset += rotated_width

    # Phase 3: Align all shapes to one side
    min_x = min([s.bounds[0] for s in current_layout])
    for i, shape in enumerate(current_layout):
        dx = -min_x
        current_layout[i] = translate(shape, xoff=dx)

    # Apply the layout
    sheet.shapes = current_layout


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
    sheet_width = 200
    sheet_height = 200
    sheet = Sheet(sheet_width, sheet_height)

    # Define the shape type and dimensions
    shape_type = "circle"  # Options: rectangle, square, circle, arc
    size1 = 15  # For rectangle, square, or circle, this is the width/diameter. For arc, this is the inner radius.
    size2 = 10  # Optional for arc (outer radius) or rectangle (height).
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