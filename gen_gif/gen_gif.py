from PIL import Image, ImageDraw, ImageFont
import os
import cv2

def add_text_to_image(image, text_to_add, right=False):
    draw = ImageDraw.Draw(image)

    font_size = 40
    font = ImageFont.truetype("ttf_all/Roboto-Regular.ttf", font_size) 

    text_color = (255, 255, 255)
    outline_color = (0, 0, 0) 

    text_bbox = draw.textbbox((10, 30), text_to_add, font=font)
    
    if right:
        text_position = (image.width - text_bbox[2] - 10, 10)
    
    else: text_position = (10, 10)
    
    shadow_color = (10, 10, 10)
    draw.text((text_position[0] + 1, text_position[1] + 1), text_to_add, font=font, fill=shadow_color)
    draw.text(text_position, text_to_add, font=font, fill=text_color)

    return image
    

# def create_gif(blurred_path, clear_path, input_path, output_path, num_frames=5, line_thickness=1, line_color="white"):
def create_gif(blurred_path, clear_path, output_path, num_frames=30, line_thickness=1, line_color="white", back_n_forth=False):
    blurred_image = Image.open(blurred_path).convert("RGB") 
    clear_image = Image.open(clear_path).convert("RGB")
    
    # blurred_image_with_text = add_text_to_image(blurred_image.copy(), 'SAM', right=True)
    # clear_image_with_text = add_text_to_image(clear_image.copy(), 'RobustSAM')

    # blurred_image_with_text = blurred_image
    # clear_image_with_text = clear_image
    blurred_image_with_text = add_text_to_image(blurred_image.copy(), 'Input', right=True)
    clear_image_with_text = add_text_to_image(clear_image.copy(), 'Output')

    width, height = blurred_image.size
    frames = []

    # Forward sweep (left to right)
    for i in range(num_frames):
        line_position = int((i / (num_frames - 1)) * width) 
        frame = Image.new("RGBA", (width, height), color=(0, 0, 0, 0))
        frame.paste(blurred_image_with_text.crop((line_position, 0, width, height)), (line_position, 0))
        frame.paste(clear_image_with_text.crop((0, 0, line_position, height)), (0, 0))
        draw = ImageDraw.Draw(frame)
        draw.rectangle([(line_position, 0), (line_position + line_thickness, height)], fill=line_color)
        frames.append(frame)

    # Backward sweep if back_n_forth = True
    if back_n_forth:
        frames_temp = frames.copy()
        for i in range(1, num_frames):
            frames.append(frames_temp[-1*i])

    frames[0].convert("RGB").save(output_path, save_all=True, append_images=frames[1:], duration=120, loop=0, format="PNG")

# def create_gif(blurred_path, clear_path, input_path, output_path, num_frames=5, line_thickness=1, line_color="white"):
def create_gif2(blurred_path, clear_path, output_path, num_frames=30, line_thickness=1, line_color="white", back_n_forth=False):
    blurred_image = Image.open(blurred_path).convert("RGB") 
    clear_image = Image.open(clear_path).convert("RGB")
    
    # blurred_image_with_text = add_text_to_image(blurred_image.copy(), 'SAM', right=True)
    # clear_image_with_text = add_text_to_image(clear_image.copy(), 'RobustSAM')

    # blurred_image_with_text = blurred_image
    # clear_image_with_text = clear_image
    blurred_image_with_text = add_text_to_image(blurred_image.copy(), 'Output', right=True)
    clear_image_with_text = add_text_to_image(clear_image.copy(), 'Input')

    width, height = blurred_image.size
    frames = []

    # Forward sweep (left to right)
    for i in range(num_frames):
        line_position = int((i / (num_frames - 1)) * width) 
        frame = Image.new("RGBA", (width, height), color=(255, 255, 255, 0))
        frame.paste(blurred_image_with_text.crop((line_position, 0, width, height)), (line_position, 0))
        frame.paste(clear_image_with_text.crop((0, 0, line_position, height)), (0, 0))
        draw = ImageDraw.Draw(frame)
        draw.rectangle([(line_position, 0), (line_position + line_thickness, height)], fill=line_color)
        frames.append(frame)

    # Backward sweep if back_n_forth = True
    if back_n_forth:
        frames_temp = frames.copy()
        for i in range(1, num_frames):
            frames.append(frames_temp[-1*i])

    frames[0].convert("RGB").save(output_path, save_all=True, append_images=frames[1:], duration=120, loop=0, format="PNG")

# save_dir = 'output' 
# os.makedirs(save_dir, exist_ok=True)

# degraded_list = ['blur', 'haze', 'lowlight', 'rain']

# for degraded_type in degraded_list:    
#     input_path = "input_images/{}-input.jpg".format(degraded_type)
#     input_img = cv2.imread(input_path)
#     cv2.imwrite(os.path.join(save_dir, '{}.jpg'.format(degraded_type)), input_img)
    
#     sam_path = "input_images/{}-sam.jpg".format(degraded_type)
#     robust_sam_path = "input_images/{}-robustsam.jpg".format(degraded_type)
    
#     output_gif_path = os.path.join(save_dir, "{}.gif".format(degraded_type))
#     create_gif(sam_path, robust_sam_path, output_gif_path, back_n_forth=False)
    
#     output_gif_path = os.path.join(save_dir, "{}_back_n_forth.gif".format(degraded_type))
#     create_gif(sam_path, robust_sam_path, output_gif_path, back_n_forth=True)


im_input_path = "diffbody/diffbody1.png"
im_output_path = "diffbody/diffbody2.png"
output_gif_path = os.path.join('diffbody', "back_n_forth2.gif")
create_gif2(im_output_path, im_input_path, output_gif_path, back_n_forth=True)