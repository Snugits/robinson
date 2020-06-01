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
#### Inference
All work with model in [detector.py](./detector.py). But let's go through by key points.

### Software

## Conclusion