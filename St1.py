import cv2
import os
import getpass

def str_to_bin(text): return ''.join(f'{ord(c):08b}' for c in text)
def bin_to_str(binary): return ''.join(chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8))

def encrypt_image(image_path, message, password, output_path="encryptedImage.png"):
    img = cv2.imread(image_path)
    if img is None: return print("Error: Image not found!")
    
    height, width, _ = img.shape
    max_bytes = height * width * 3 // 8
    binary_message = str_to_bin(password + "|" + message)
    
    if len(binary_message) > max_bytes * 8: return print("Error: Message too long.")
    
    binary_message = f"{len(binary_message):032b}" + binary_message
    idx = 0

    for i in range(height):
        for j in range(width):
            for k in range(3):
                if idx < len(binary_message):
                    img[i, j, k] = (img[i, j, k] & 254) | int(binary_message[idx])
                    idx += 1
                else: break

    cv2.imwrite(output_path, img)
    os.system(f"start {output_path}") 
    print("Message encrypted successfully.")

def decrypt_image(image_path, entered_password):
    img = cv2.imread(image_path)
    if img is None: return print("Error: Image not found!")

    binary_data = ''.join(str(img[i, j, k] & 1) for i in range(img.shape[0]) for j in range(img.shape[1]) for k in range(3))
    message_length = int(binary_data[:32], 2)

    if message_length <= 0 or message_length > len(binary_data) - 32: return print("Decryption failed.")
    
    extracted_message = bin_to_str(binary_data[32:32 + message_length])
    if '|' not in extracted_message: return print("Decryption failed: Incorrect format.")

    stored_password, secret_message = extracted_message.split('|', 1)
    
    if entered_password == stored_password:
        print("Decryption successful! Hidden message:", secret_message)
    else:
        print("YOU ARE NOT AUTHORIZED!")

if __name__ == "__main__":
    hide_passcode_enc = input("User, do you want to hide the passcode before encryption? (yes/no): ").strip().lower()
    password = getpass.getpass("Enter a passcode: ") if hide_passcode_enc == "yes" else input("Enter a passcode: ")
    message = input("Enter secret message: ")
    encrypt_image("house.png", message, password)
    
    hide_passcode_dec = input("User, do you want to hide the passcode before decryption? (yes/no): ").strip().lower()
    entered_password = getpass.getpass("Enter passcode: ") if hide_passcode_dec == "yes" else input("Enter passcode: ")
    decrypt_image("encryptedImage.png", entered_password)