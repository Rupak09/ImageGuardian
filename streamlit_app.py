import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

# Function for image encryption
def encrypt_images(images, params):
    encrypted_images = []

    for image in images:
        # Extract RGB values from the original image
        rgb_array = np.array(image)

        # Your encryption logic goes here
        # For illustration, let's just display the original and encrypted images
        plt.subplot(1, 2, 1)
        plt.imshow(rgb_array)
        plt.title('Original Image')
        plt.axis('off')

        # Placeholder for encryption logic
        # Replace this with your actual encryption code
        encrypted_array = image1

        plt.subplot(1, 2, 2)
        plt.imshow(image1)
        plt.title('Encrypted Image')
        plt.axis('off')

        plt.show()

        encrypted_images.append(Image.fromarray(encrypted_array))

    return encrypted_images

# Function for image decryption
def decrypt_images(images, params):
    decrypted_images = []

    for image in images:
        # Extract RGB values from the original image
        rgb_array = np.array(image)

        # Your decryption logic goes here
        # For illustration, let's just display the original and decrypted images
        plt.subplot(1, 2, 1)
        plt.imshow(rgb_array)
        plt.title('Original Image')
        plt.axis('off')

        # Placeholder for decryption logic
        # Replace this with your actual decryption code
        decrypted_array = pixel_image

        plt.subplot(1, 2, 2)
        plt.imshow(decrypted_array)
        plt.title('Decrypted Image')
        plt.axis('off')

        plt.show()

        decrypted_images.append(Image.fromarray(decrypted_array))

    return decrypted_images
# Streamlit UI layout
def main():
    st.title('Multiple Image Encryption and Decryption')

    # Sidebar for parameters
    st.sidebar.title("Settings")
    # Example parameter - adjust as needed for the algorithm
    param1 = st.sidebar.slider('Parameter 1', 0, 100, 50)

    # Image upload section
    st.subheader("Upload Images for Encryption/Decryption")
    uploaded_files = st.file_uploader("Choose Images", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])

    if uploaded_files:
        images = [Image.open(file) for file in uploaded_files]

        # Encrypt Images
        if st.button('Encrypt Images'):
            encrypted_images = encrypt_images(images, [param1])
            st.subheader("Encrypted Images")
            for img in encrypted_images:
                st.image(img, caption='Encrypted Image', use_column_width=True)

        # Decrypt Images
        if st.button('Decrypt Images'):
            decrypted_images = decrypt_images(images, [param1])
            st.subheader("Decrypted Images")
            for img in decrypted_images:
                st.image(img, caption='Decrypted Image', use_column_width=True)

if __name__ == "__main__":
    main()
