import sys
import qrcode
import logging.config
from pathlib import Path
import os
import argparse
from datetime import datetime
import validators 


QR_DIRECTORY = os.getenv('QR_CODE_DIR', 'qr_codes')
FILL_COLOR = os.getenv('FILL_COLOR','purple')
BACK_COLOR = os.getenv('BACK_COLOR','white')

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
def create_dir(path: Path):
    try:
        path.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        logging.error(f"Failed to create directory at {path}: {e}")
        exit(1)
def valid_url(url):
    if validators.url(url):
        return True
    else:
        logging.error(f"Invalid URL: {url}")
        return False
    
def generate_qr_code(data, path, fill_color='purple',back_color='white'):
    if not valid_url(data):
        return
    try:
        qr =qrcode.QRCode(version=1,box_size=10,border=5)
        qr.add_data(data)
        qr.make(fit=True)
        image = qr.make_image(fill_color = fill_color, back_color=back_color)
        
        with path.open('wb') as qr_file:
            image.save(qr_file)
        logging.info(f"QR Code successfuly created and saved to {path}")

    except Exception as e:
        logging.error(f"An error occured in the process of Generating/Saving the QR Code: {e}")

def main():
    parser =argparse.ArgumentParser(description='Please Generate a QR Code')
    parser.add_argument('--url', help="URL that will be encoded",default='https://github.com/oae26')
    args = parser.parse_args()

    setup_logging()

    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    qr_filename = f"QRCode_{timestamp}.png"

    qr_code_full_path = Path.cwd() /QR_DIRECTORY/qr_filename

    create_dir(Path.cwd()/QR_DIRECTORY)

    generate_qr_code(args.url, qr_code_full_path, FILL_COLOR, BACK_COLOR)

if __name__ == "__main__":
    main()