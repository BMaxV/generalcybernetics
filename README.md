# generalcybernetics

Eh. This is a little project to set up simple graphs that I used and plan to reuse.

![simplepicture](this_test.svg)

So far, the "cyber" part of this repo wasn't really "cyber"ing very much
It was a module to build some graphs with, with the option of giving
the nodes "stuff" and the ability to be nested.

Now, I have added some "calculation container objects" that can actually
do stuff with the graph and I have built a simple control loop with it and that works.

![loop](tests/simple_loop.jpg)

The way this is done is in the test functions, but it is a bit annoying
and some writeup might help.

Since I also want to do a GUI for this, I made some choices:

blender's nodes, as a prominent example, have lots of in, outputs and
that's great, because they serve as a way to actually do data input.

I want something that's mostly about structure and which inputs go where
and what they should be like, should be driven by input data and not
necessarily user input.

Really the only thing that matters at that point is the connection structure
between nodes. I am delegating the exact logic on what happens, which
variables get used and how, to code.

This has the advantage of being very simple on that level and the disadvantage
that all the nice regular things we do with python, like *args **kwargs
optional stuff and passing values by position don't really work that well anymore.

But the upside is that I can now produce a very simple, clean save file
that describes the interconnectedness of functions and we gain more
control over execution time or errors in those functions.

Unfortunately all of that means, that the names of the variables that 
the functions  in the control loop should fetch from the single dictionary
that's being passed around, have to be defined in advance and that should look like this:
 
```py

N1 = basis.Element("input")
N2 = basis.Element("action")
N3 = basis.Element("compare")
N4 = basis.Element("feedback")

value_dict = {"value":0,"action":False,"target":-0.3,"reduce_amount":0.1,"compare_result":False}

N1.payload = basis.InputObject(value_dict)
N2.payload = basis.CyberCalculationPayload(basis.myaction,datakeywords = ["action","value","reduce_amount"])
N3.payload = basis.CyberCalculationPayload(basis.compare,datakeywords = ["value","target"])
N4.payload = basis.CyberCalculationPayload(basis.myfeedback,datakeywords = ["value","compare_result","action"])

N1.connect_lr(N2)
N2.connect_lr(N3)
N3.connect_lr(N4)
N4.connect_lr(N1)
```

I'm not sure if this is a good idea yet, it feels like lots of complexity.
