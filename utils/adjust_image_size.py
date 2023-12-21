from bs4 import BeautifulSoup
import chardet
import re

def replace_img_urls(file_path):
    with open(file_path, 'r+', encoding='utf-8') as file:
        content = file.read()

        # Regular expression to find image tags and capture the src attribute
        pattern = r'<img [^>]*src="([^"]+)"'
        modified_content = re.sub(pattern, lambda match: '<img src="./' + match.group(1).split('/')[-1] + '"', content)

        file.seek(0)
        file.write(modified_content)
        file.truncate()

def adjust_image_size(html_file_path):
    with open(html_file_path, 'rb') as file:
        rawdata = file.read()
        result = chardet.detect(rawdata)
        encoding = result['encoding']

    with open(html_file_path, 'r', encoding=encoding) as file:
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
        if len(sys.argv) > 2:
            replace_img_urls(sys.argv[1])
    else:
        print("Provide the path to the HTML file as an argument.")
