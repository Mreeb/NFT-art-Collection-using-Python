from turtle import color
from PIL import Image, ImageDraw, ImageChops
import random

from cv2 import borderInterpolate
from numpy import reciprocal

def random_color():
    return (random.randint(0,255), random.randint(0,255), random.randint(0,255))

def gradiant_color(start_color, end_color, factor : float):
    reciprocal = 1 - factor
    return(
        int(start_color[0] * reciprocal + end_color[0] * factor),
        int(start_color[1] * reciprocal + end_color[1] * factor),
        int(start_color[2] * reciprocal + end_color[2] * factor),
    )
 
def generate_art(path : str):
    print("GENERATING >")

    # CREATING BACKGROUND 
    image_size_px = 4000
    image_bg_color = (0,0,0)
    padding_px = 400 # FOR ADDING A LITTLE PADDING TO THE LINES 
    starting_color = random_color()
    ending_color = random_color()

    image = Image.new(mode="RGB",  size=(image_size_px,image_size_px),  color=image_bg_color)

    draw = ImageDraw.Draw(image)

    points = list()

    # GENERATING THE POINTS 
    for _ in range(80):
        random_p = (
            random.randint(padding_px, image_size_px - padding_px),
            random.randint(padding_px, image_size_px - padding_px)
        )
        points.append(random_p)

    
    # DRAW A BOUNDING BOX
    min_x = min([p[0] for p in points])
    max_x = max([p[0] for p in points])
    min_y = min([p[1] for p in points])
    max_y = max([p[1] for p in points])
 
    #CENTERING THE IMAGE
    delta_x = min_x - (image_size_px - max_x)
    delta_y = min_y - (image_size_px - max_y)


    for i, point in enumerate(points):
        points[i] = (point[0] - delta_x // 2, point[1])
        points[i] = (point[0] - delta_y // 2, point[1])

    # DRWAING LINES IN SUCH A WAY THAT THE LAST POINT CONNECTS TO THE LAST POINT 
    thickness = 10 
    n_points = len(points) - 1
    for i, point in enumerate(points):

        overlay_image = Image.new(mode="RGB",  size=(image_size_px,image_size_px),  color=image_bg_color)

        overlay_draw = ImageDraw.Draw(overlay_image)

        p1 = point
        
        if i == n_points: p2 = points[0]
        else: p2 = points[i + 1]

        color_factor = i / n_points
        line_color = gradiant_color(starting_color,ending_color,color_factor)
        line_xy = (p1,p2)
        thickness += 1
        overlay_draw.line(line_xy,fill=line_color,width=thickness)
        image = ImageChops.add(image, overlay_image)

    # SAVING THE IMAGE
    image.save(path)
 
if __name__ == "__main__":
    for Image_no in range(30):
        generate_art(f"test_image_{Image_no}.png")