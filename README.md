 The library has tools to validate PAN card issued by the Indian Income Tax Department.
 
 It has a suite of functions with varying level of speed and accuracy to do the following:
 1. Quickly detect PAN card in the image.
 2. Run Pixel Bit error detection to predict if the image is Photoshopped, along with the confidence level and areas that might be photoshopped.
 3. Do OCR and extract the required details like Name, Father's Name, DOB, PAN number from the image. With validation and confidence level of the extraction for each field.
 4. Feed back errors with OCR, by a Human Operator to help the system perform better in the future.
 5. Data is saved to Mongo and rendered instantly for verification using Meteor.
 
