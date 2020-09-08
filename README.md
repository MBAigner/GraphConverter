# Graph Converter

The Graph Converter is a tool for creating a graph representation out of the content of PDFs.
A graph representation can act as the basis for further document processing steps.
Geometric relationships are encapsulated. By those, a document structure can be retrieved.

The tool works independent of different document layouts.
The graph construction can be controlled via parameter settings mentioned subsequently.
Furthermore, layout-based optimizations without the need parameter tweaks are supported using a regression estimation based on document layout characteristics.

The processing of PDF documents is done using the ```PDFContentConverter``` library.

## How-to

* Pass the path of the PDF file which is wanted to be converted to ```GraphConverter```.
* Call the function ```convert()```. The document graph representations are returned page-wise as a list of ```networkx``` graphs.
* Media boxes of a PDF can be accessed using ```get_media_boxes()```, the page count over ```get_page_count()```

Example call: 

    converter = GraphConverter(pdf)
    result = converter.convert()

Beside the graph conversion, media boxes of a document can be accessed using ```get_media_boxes()``` and the page count over ```get_page_count()```.
General document characteristics are stored in a ```converter.meta``` object.

A more detailed example usage is also given in ```Tester.py```.

## Example

The following image shows a resulting document graph representation when using the ```GraphConverter```.
TODO

## Settings

TODO describe meta characteristics, thresholds, ...

## Project Structure

* ```GraphConverter.py```: contains the ```GraphConverter``` class for converting documents into graphs.
* ```util```:
  * ```constants```: 
  * ```StorageUtil```: store/load functionalities
* ```Tester.py```: Python script for testing the ```GraphConverter```
* ```pdf```: example pdf input files for tests

## Output Format

As a result, a list of ```networkx``` graphs is returned.
Each graph encapsulates a structured representation of a single page.

Edges are attributed with the following features:

* ```direction```: shows the direction of an edge.
    * ```v```: Vertical edge
    * ```h```: Horizontal edge
    * ```l```: Rectangular loop. This represents a novel concept encapsulating structural characteristics of document segments by observing if two different paths end up in the same node.
* ```length```: Scaled length of an edge
* ```lengthx_phys```: Horizontal edge length
* ```lengthy_phys```: Vertical edge length
* ```weight```: Scaled total length

All nodes contain the following content attributes:

* ```id```: unique identifier of the PDF element
* ```page```: page number, starting with 0
* ```text```: text of the PDF element
* ```x_0```: left x coordinate
* ```x_1```: right x coordinate
* ```y_0```: top y coordinate
* ```y_1```: bottom y coordinate
* ```pos_x```: center x coordinate
* ```pos_y```: center y coordinate
* ```abs_pos```: tuple containing a page independent representation of ```(pos_x,pos_y)``` coordinates
* ```original_font```: font as extracted by pdfminer
* ```font_name```: name of the font extracted from ```original_font```
* ```code```: font code as provided by pdfminer
* ```bold```: factor 1 indicating that a text is bold and 0 otherwise
* ```italic```: factor 1 indicating that a text is italic and 0 otherwise
* ```font_size```: size of the text in points
* ```masked```: text with numeric content substituted as #
* ```frequency_hist```: histogram of character type frequencies in a text, stored as a tuple containing percentages of textual, numerical, text symbolic and other symbols
* ```len_text```: number of characters
* ```n_tokens```: number of words
* ```tag```: tag for key-value pair extractions, indicating keys or values based on simple heuristics
* ```box```: box extracted by pdfminer Layout Analysis
* ```in_element_ids```: contains IDs of surrounding visual elements such as rectangles or lists. They are stored as a list [left, right, top, bottom]. -1 is indicating that there is no adjacent visual element.
* ```in_element```: indicates based on in_element_ids whether an element is stored in a visual rectangle representation (stored as "rectangle") or not (stored as "none").

The media boxes possess the following entries in a dictionary:

* ```x0```: Left x page crop box coordinate
* ```x1```: Right x page crop box coordinate
* ```y0```: Top y page crop box coordinate
* ```y1```: Bottom y page crop box coordinate
* ```x0page```: Left x page coordinate
* ```x1page```: Right x page coordinate
* ```y0page```: Top y page coordinate
* ```y1page```: Bottom y page coordinate


## Future Work

* The ```GraphConverter``` will be extended using OCR processing for images in order to support more unstructured types than solely PDFs.

## Acknowledgements

* Example PDFs are obtained from the ICDAR Table Recognition Challenge 2013 https://roundtrippdf.com/en/data-extraction/pdf-table-recognition-dataset/.

## Authors

* Michael Benedikt Aigner
* Florian Preis
