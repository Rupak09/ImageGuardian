import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import streamlit as st
import os
from image_encryption_in_py import (
    map_to_dna,
    convert_to_rna,
    mutate_rna,
    translate_rna,
    binary_to_pixels,
    reverse_translate_rna_array,
    reverse_convert_to_dna,
    reverse_map_to_dna,
    unscramble_matrix
)


# Function for image encryption
def encrypt_images(image_paths, params):
    encrypted_images = []

    for image_path in image_paths:
        # Extract RGB values from the original image
        image = Image.open(image_path)
        rgb_array = np.array(image)

        # Convert the RGB image to grayscale image
        gray_image = image.convert('L')

        # Convert to numpy array and then to 8-bit binary
        gray_array = np.array(gray_image)

        # Create bit planes
        bit_planes = np.unpackbits(np.expand_dims(gray_array, axis=-1), axis=-1)
        bit_planes_3d = bit_planes.reshape(gray_array.shape + (8,))

        # Stack all bit planes horizontally to form a 3D cube
        bit_cube = np.concatenate([bit_planes_3d[:, :, 7 - bit][:, :, np.newaxis] for bit in range(8)], axis=-1)

        # Shuffle the binary values in the 3D matrix
        shuffled_bit_planes_3d = 1 - bit_planes_3d

        # Convert to DNA sequences
        mapped_dna_array = map_to_dna(shuffled_bit_planes_3d)

        # Convert DNA to RNA
        mapped_rna_array = np.empty_like(mapped_dna_array)
        for i in range(mapped_dna_array.shape[0]):
            for j in range(mapped_dna_array.shape[1]):
                mapped_rna_array[i, j] = convert_to_rna(mapped_dna_array[i, j])

        # RNA mutation
        mutated_rna_array = np.empty_like(mapped_rna_array)
        for i in range(mapped_rna_array.shape[0]):
            for j in range(mapped_rna_array.shape[1]):
                mutated_rna_array[i, j] = mutate_rna(mapped_rna_array[i, j])

        # RNA translation
        translated_rna_array = np.empty_like(mutated_rna_array)
        for i in range(mutated_rna_array.shape[0]):
            for j in range(mutated_rna_array.shape[1]):
                translated_rna_array[i, j] = translate_rna(mutated_rna_array[i, j])

        # Convert RNA to binary
        binary_array = np.zeros_like(translated_rna_array, dtype=int)
        for i in range(translated_rna_array.shape[0]):
            for j in range(translated_rna_array.shape[1]):
                for k, base in enumerate(translated_rna_array[i, j]):
                    binary_array[i, j, k * 2:k * 2 + 2] = [int(x) for x in rna_rules[base]]

        # Display the encrypted image
        encrypted_image = binary_to_pixels(binary_array)
        st.image(encrypted_image, caption='Encrypted Image', use_column_width=True, channels="L", format="PNG")

        encrypted_images.append(Image.fromarray(encrypted_image))

    return encrypted_images

# Function for image decryption
def decrypt_images(image_paths, params):
    decrypted_images = []

    for image_path in image_paths:
        # Extract RGB values from the original image
        image = Image.open(image_path)
        rgb_array = np.array(image)

        # Extract binary data from the encrypted image
        binary_array = pixels_to_binary(np.array(rgb_array))

        # Reverse the encryption process
        reversed_rna_array = reverse_translate_rna_array(binary_array)
        reversed_2d_rna_array = reverse_translate_rna_array(reversed_rna_array)

        reversed_dna_to_rna_array = np.empty_like(mapped_rna_array, dtype='object')
        for i in range(mapped_rna_array.shape[0]):
            for j in range(mapped_rna_array.shape[1]):
                rna_seq = mapped_rna_array[i, j]
                reversed_seq = reverse_convert_to_dna(rna_seq)
                reversed_dna_to_rna_array[i, j] = reversed_seq

        reversed_bit_planes_3d = reverse_map_to_dna(reversed_dna_to_rna_array)
        unscrambled_bit_planes_3d = unscramble_matrix(reversed_bit_planes_3d)

        # Convert to pixel values
        pixel_image = binary_to_pixels(unscrambled_bit_planes_3d)

        # Display the decrypted image
        st.image(pixel_image, caption='Decrypted Image', use_column_width=True, channels="L", format="PNG")

        decrypted_images.append(Image.fromarray(pixel_image))

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
