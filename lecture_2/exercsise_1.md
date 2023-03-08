# Asynchronous programming

### Distributed applications often require going "off the main thread" to perform


### SQL queries are synchronous, and can take a long time to complete. We can use the `asyncio` library to run them in the background.

#### Example
* cooking pasta is a good example of a long-running synchronous task. Task-by-task  = Slow
* Asynchronous programming is a way to run multiple tasks at the same time.  = Fast
  

## Asyncio is a library that allows us to write concurrent code using the `async` and `await` syntax.

#### Example = we only have one thread, but we can run multiple tasks at the same time

 ```python
    import asyncio
    import time

    async def mycoroutine(args):
        # do something
        await call()

    async def main():
        await asyncio.gather(
            mycoroutine(args),
            mycoroutine(args),
            mycoroutine(args),
        )

    if __name__ == "__main__":
        start = time.perf_counter()
        asyncio.run(main())
        end = time.perf_counter()
        print(f"Finished in {end - start} seconds")
```


```python
import sys
import asyncio
from codetiming import Timer


async def boil_water():
    """
    Boiling water takes 5 seconds.
    :return:
    """
    print("Boiling water", end="...")
    await asyncio.sleep(5)
    print("Done boiling water")


async def prepare_salad():
    """
    Preparing a good salad requires 10 seconds
    :return:
    """
    print("Preparing salad", end="...")
    await asyncio.sleep(10)
    print("Done preparing salad")


async def cook_spaghetti():
    """
    Spaghetti are done after 7 seconds in boiling water.
    :return:
    """
    print("Cooking spaghetti", end="...")
    await asyncio.sleep(7)
    print("Done cooking spaghetti")


async def cook_sauce():
    """
    Grandma's secret tomato sauce: 4 seconds
    :return:
    """
    print("Cooking tomato sauce", end="...")
    await asyncio.sleep(4)
    print("Done cooking sauce")


async def prepare_lunch():
    """
    Let's cook for lunch!
    :return:
    """
    with Timer(text="Total elapsed time {:.1f}"):

        #we are going to run the tasks in parallel using asyncio.gather
        #asyncio.create_task is a coroutine that creates a task from a coroutine = for us boil_water() is a coroutine

        #2 blocks runing sequentially but inside of each block it is parallel
        await asyncio.gather(asyncio.create_task(boil_water()),
                       asyncio.create_task(prepare_salad())
                          )


        await asyncio.gather(asyncio.create_task(cook_spaghetti()),
                       asyncio.create_task(cook_sauce())
                          )
              
        print("Ready for lunch!")


if __name__ == "__main__":
    asyncio.run(prepare_lunch())


```


 ```
    await def mycouroutine(args):
        # do something
        await call()```

defines a coroutine