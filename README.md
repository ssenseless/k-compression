## K-Compressor v1.1.1
> Fairly functional application that allows users to compress images down to a specified number of colors, view some of the colors (k-means centroids) used in the compression, and save the compressed image. 

### Current features
* Functioning k-means compression
* .png/.jpg support
* Color preview on bottom
* Photo saving functionality (updated to retain aspect ratio and pixel structure of original image while retaining speed of functionality)
* Implemented functionality for non-square photos
* Vectorized compression algorithm (98.9% time reduction)
* Auto-fills extensions when saving compressed photos
* Color preview now shows top 6 colors, relevant percentage amounts, and the remaining amount off to the side
* Full code documentation
* Aspect ratio limitation to ensure app can function (at least the largest of the height and width of the original, at most 1000 for either)

### Upgrade Steps
* Small text errors (e.g. "remaining 1 colors")
* Versioning for Mac/Linux?

### Application image
![k-compress](https://github.com/user-attachments/assets/53f61ed9-4bd3-4ad2-b983-b566e18a6ed5)
