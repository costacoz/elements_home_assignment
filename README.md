# Elements home-assignment
This project contains the results of home-assignment from Elements company.

## Tests
Executable test are located in **csv_proc/tests.py.**

## How CSV file is loaded
The URL to CSV file is located in `settings.py` and is being used in `/process_csv/` API endpoint. 

## Mobile friendly images
Mobile friendly resolution is considered to be maximum of 500px width and 500px height.
If the image is greater than that, then it is resized respecting the aspect ratio.

## How image caching is implemented
Image caching is done by avoiding downloading of image multiple time.

There is an `processed_images` dict variable that contains image urls as a key and processed image (converted to base64 and optimized for mobile) as a value.

## Application structure
Image and CSV files computations are carried out to `helper.py` helper classes for structuring and readability puproses.

## Performance


## Working in DTAP
There are 4 branches in this repository:
* Development (**dev**)
* Testing (**test**)
* Acceptance (**accept**)
* Production (**main**)

The work was done in this sequence: 
* A local branch is created and work is done in local branch
* The local branch is merged to **dev** branch
* **dev** branch is merged to **test** branch
* **test** branch is merged to **accept** branch
* **accept** branch is merged to **main** branch

## Exception handling
Exception handlings were used throughout the project extensively per task requirements.

## Response cache
Response cache is implemented using `@cache_page` decorator for the view function.

## Scalability

