Inference or prediction of a task returns a list of `Results` objects. Alternatively, in the streaming mode, it returns a generator of `Results` objects which is memory efficient. Streaming mode can be enabled by passing `stream=True` in predictor's call method.

!!! example "Predict"
    === "Getting a List"
        ```python
        inputs = [img, img] # list of np arrays
        results = model(inputs) # List of Results objects
        for result in results:
            boxes = result.boxes # Boxes object for bbox outputs
            masks = result.masks # Masks object for segmenation masks outputs
            probs = result.probs # Class probabilities for classification outputs
            ...
        ```
    === "Getting a Generator"
        ```python
        inputs = [img, img] # list of np arrays
        results = model(inputs, stream=True) # Generator of Results objects
        for result in results:
            boxes = result.boxes # Boxes object for bbox outputs
            masks = result.masks # Masks object for segmenation masks outputs
            probs = result.probs # Class probabilities for classification outputs
            ...
        ```

## Working with Results

Results object consists of these component objects:

- `results.boxes` : It is an object of class `Boxes`. It has properties and methods for manipulating bboxes
- `results.masks` : It is an object of class `Masks`. It can be used to index masks or to get segment coordinates.
- `results.prob`  : It is a `Tensor` object. It contains the class probabilities/logits.

Each result is composed of torch.Tensor by default, in which you can easily use following functionality:
```python
results = results.cuda()
results = results.cpu()
results = results.to("cpu")
results = results.numpy()
```
### Boxes
`Boxes` object can be used index, manipulate and convert bboxes to different formats. The box format conversion operations are cached, which means they're only calculated once per object and those values are reused for future calls.

- Indexing a `Boxes` objects returns a `Boxes` object
```python
boxes = results.boxes
box = boxes[0] # returns one box
box.xyxy 
```
- Properties and conversions
```
boxes.xyxy   # box with xyxy format, (N, 4)
boxes.xywh   # box with xywh format, (N, 4)
boxes.xyxyn  # box with xyxy format but normalized, (N, 4)
boxes.xywhn  # box with xywh format but normalized, (N, 4)
boxes.conf   # confidence score, (N, 1)
boxes.cls    # cls, (N, 1)
boxes.data   # raw bboxes tensor, (N, 6) or boxes.boxes .
```
### Masks
`Masks` object can be used index, manipulate and convert masks to segments. The segment conversion operation is cached.

```python
masks = results.masks # Masks object
masks.segments  # bounding coordinates of masks, List[segment] * N
masks.data      # raw masks tensor, (N, H, W) or masks.masks 
```

### probs
`probs` attribute of `Results` class is a `Tensor` containing class probabilities of a classification operation.
```python
results.probs     # cls prob, (num_class, )
```

Class reference documentation for `Results` module and its components can be found [here](reference/results.md)
