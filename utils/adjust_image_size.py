from bs4 import BeautifulSoup

def adjust_image_size(html_file_path):
    with open(html_file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
        
    # Find all image tags
    for img_tag in soup.find_all('img'):
        # Remove width and height attributes to let the image be of its original size
        if 'width' in img_tag.attrs:
            del img_tag.attrs['width']
        if 'height' in img_tag.attrs:
            del img_tag.attrs['height']
            
    # Write the modified HTML back to the file
    with open(html_file_path, 'w', encoding='utf-8') as file:
        file.write(str(soup))

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        adjust_image_size(sys.argv[1])
    else:
        print("Provide the path to the HTML file as an argument.")