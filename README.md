# Robinson - the robot that protects your belongings from cat curiosity

* [The main problem](#the-main-problem)
* [Idea](#idea)
* [Realization](#realization)
  * [Hardware](#hardware)
  * [ML](#ml)
  * [Software](#software)
* [Conclusion](#conclusion)

## The main problem
{фото помидора}
I have a curious cat. And nothing can't happen without her participation in the flat. She adores bites plants and destroys the Christmas tree. And it is bad for me.
## Idea
Idea is to create a system that will scare away from a particular place. First in my mind came thought to scare it like dogs with a special whistle. But for cats, it doesn't work and some noise at night bad for my mind healthy.
So I need something soundless and something that might work at night. Bingo! IR camera + Raspberry Pi + Water pump.
## Realization
### Hardware
My Supplies:
 * Raspberry PI 3B {фото}
 * Water Pump {фотку} I bought on AliExpress
 * Pi NoIR Camera V2 {фото}
 * Current relay (I had already had a module with two relays but indeed it is require only one) {фото}
 * Lego

### Software


### ML
This article is not about how to train model. I'm a programmer, but I'm interested in Data Science. And here I show how to use a model in a script.
#### Model
I got pre-trained model MobileNet V2 and got on training with dataset cats_vs_dogs. [Here is a tutorial](https://www.tensorflow.org/tutorials/images/transfer_learning)
#### Convert to tflite 
The output I got .pb file and folder with some variables but I needed to convert it to .tflite.\
I used a [docker image](https://hub.docker.com/r/tensorflow/tensorflow/) with TensorFlow (I didn't want to install TF on my PC). And here how easily you can convert your model:\
`tflite_convert  --output_file=./model.tflite  --saved_model_dir=/model`\
**--output_file** - Path where you want to save converted model\
**--saved_model_dir** - Path to folder which you've saved with `tf.saved_model.save`
#### Detector's work
All work with model in [detector.py](./detector.py). But let's go through by key points.
First, we need class `Detector` and only two public methods: `check` and `is_detect` so simple.\
Every calling of `check` will take a picture and try to recognize objects, after that we should ask is there any detections: `is_detect`.

#### Inference
We need to create `Interpreter` and pass the path to our converted `.tflite` model. After that we can get info about tensors by `get_input_details()`. But we need to know only about first (input) tensor `get_input_details()[0]` - will return dict, where we need get key `shape` and there we have array like this: `[  1, 160, 160,   3]`.
 * First element (_1_) it is how many images accepts our model
 * Second and third elements (_160, 160_) it is size of our image
 * The last one (_3_) it is how many channels in the image (for RGB - 3, for gray - 1)
 
So we need to get the size of an image to resize to it all input images and we achieve it with slice `[1:3]`. Let's record value to `__img_input_size` .\
Let's analyze another key point `self.__interpreter.tensor(tensor_index)()[0][:, :] = image`\
Here we `self.__interpreter.tensor(tensor_index)` retrieve tensor by `tensor_index` (was retrieved from info like input size) this calling will return another function and we at once call it. Result will zero-matrix with shape _(1, 160, 160, 3)_ like we got in `get_input_details()`.\
As we know the first element is a count of images that tensor accepts, so we need to get the first element `self.__interpreter.tensor(tensor_index)()[0]`.\
And further tricky moment `[:, :] = image` at right side _(shape (160, 160, 3))_ we get each element and rewrite it by each corresponded element from the left side. _(image it is already converted and resized picture from camera)_. So, we "placed" picture from the camera into a tensor.\
After that we call `self.__interpreter.invoke()` it makes calculation magic and get the result `self.__interpreter.get_output_details()[0]`\
In the result we get number and result < 0 means that network detects first class object, result > 0 - second class object. And the more further from zero, the more confident result.

## Conclusion