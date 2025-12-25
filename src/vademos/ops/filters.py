import cv2
import numpy as np

def apply_clahe(image: np.ndarray, clip_limit: float = 2.0, tile_grid_size: tuple = (8, 8)) -> np.ndarray:
    """
    Apply Contrast Limited Adaptive Histogram Equalization (CLAHE).
    Expects BGR or Grayscale image. Returns same format.
    """
    if len(image.shape) == 3:
        # Convert to LAB for better color preservation
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
        l = clahe.apply(l)
        lab = cv2.merge((l, a, b))
        return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    else:
        # Grayscale
        clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
        return clahe.apply(image)

def apply_unsharp_mask(image: np.ndarray, gaussian_kernel: tuple = (5, 5), sigma: float = 1.0, amount: float = 1.0, threshold: int = 0) -> np.ndarray:
    """
    Sharpen image using Unsharp Masking.
    sharpened = original + (original - blurred) * amount
    """
    blurred = cv2.GaussianBlur(image, gaussian_kernel, sigma)
    sharpened = float(amount + 1) * image - float(amount) * blurred
    sharpened = np.clip(sharpened, 0, 255)
    
    if threshold > 0:
        low_contrast_mask = np.abs(image - blurred) < threshold
        np.copyto(sharpened, image, where=low_contrast_mask)
        
    return sharpened.astype(np.uint8)

def apply_denoise(image: np.ndarray, h: float = 10, hColor: float = 10) -> np.ndarray:
    """
    Apply Fast Non-Local Means Denoising.
    Note: This is computationally expensive.
    """
    if len(image.shape) == 3:
        return cv2.fastNlMeansDenoisingColored(image, None, h, hColor, 7, 21)
    else:
        return cv2.fastNlMeansDenoising(image, None, h, 7, 21)

def apply_adaptive_threshold(image: np.ndarray, block_size: int = 11, C: int = 2) -> np.ndarray:
    """
    Apply Adaptive Thresholding (Gaussian C).
    Input must be grayscale.
    """
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    
    # Block size must be odd
    if block_size % 2 == 0:
        block_size += 1
        
    return cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, block_size, C)
