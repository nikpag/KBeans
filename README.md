# KBeans

We get it; the K-means algorithm is 🎉amazing!🎉

But you know what else is amazing? _Speed_.

So how do we make it faster?

We run things in parallel!

![](assets/double-team.gif)

This repository is an attempt to speed up the K-means algorithm by running it in parallel. We use OpenMP, CUDA, and MPI. We then evaluate our implementations and pat ourselves on the back for the good job we did :-)

There's a folder for each platform. The OpenMP folder has some extra material on how we can use smarter locks to achieve lower contention times.
