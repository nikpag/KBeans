#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <sys/time.h>
#include "mpi.h"
#include "utils.h"

int main(int argc, char **argv)
{
    int rank, size;

    // Global matrix dimensions and local matrix dimensions (2D-domain, 2D-subdomain)
    int global[2], local[2];

    // Padded global matrix dimensions (if padding is not needed, global_padded=global)
    int global_padded[2];

    // Processor grid dimensions
    int grid[2];

    int i, j, t;

    // Flags for convergence, global and per process
    int global_converged = 0, converged = 0;

    // Dummy datatype used to align user-defined datatypes in memory
    MPI_Datatype dummy;

    // Timers: Total -> tts, ttf; Computation -> tcs, tcf; conVergence -> tvs, tvf;
    struct timeval tts, ttf, tcs, tcf, tvs, tvf;

    double ttotal = 0, tcomp = 0, tconv = 0, total_time, comp_time, conv_time;

    // Global matrix, local current and previous matrices, pointer to swap between current and previous
    double **U, **u_current, **u_previous, **swap;

    MPI_Init(&argc, &argv);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);

    //----Read 2D-domain dimensions and process grid dimensions from stdin----//

    if (argc != 5) {
        fprintf(stderr, "Usage: mpirun ... ./exec X Y Px Py\n");
        exit(-1);
    }
    else {
        global[0] = atoi(argv[1]);
        global[1] = atoi(argv[2]);
        grid[0] = atoi(argv[3]);
        grid[1] = atoi(argv[4]);
    }


    //----Create 2D-cartesian communicator----//
	//----Usage of the cartesian communicator is optional----//

    // The new 2D-cartesian communicator
    MPI_Comm CART_COMM;

    // The 2D-grid is non-periodic
    int periods[2] = {0, 0};

    // The position of each process on the new communicator
    int rank_grid[2];

    // Communicator creation
    MPI_Cart_create(MPI_COMM_WORLD, 2, grid, periods, 0, &CART_COMM);

    // Rank mapping on the new communicator
    MPI_Cart_coords(CART_COMM, rank, 2, rank_grid);

    //----Compute local 2D-subdomain dimensions----//
    //----Test if the 2D-domain can be equally distributed to all processes----//
    //----If not, pad 2D-domain----//

    for (i = 0; i < 2; i++) {
        if (global[i] % grid[i] == 0) {
            local[i] = global[i] / grid[i];
            global_padded[i] = global[i];
        }
        else {
            local[i] = (global[i] / grid[i]) + 1;
            global_padded[i] = local[i] * grid[i];
        }
    }

    //----Allocate global 2D-domain and initialize boundary values----//
    //----Rank 0 holds the global 2D-domain----//
    if (rank == 0) {
        U = allocate2d(global_padded[0], global_padded[1]);
        init2d(U, global[0], global[1]);
    }

    //----Allocate local 2D-subdomains u_current, u_previous----//
    //----Add a row/column on each size for ghost cells----//
    u_previous = allocate2d(local[0] + 2, local[1] + 2);
    u_current = allocate2d(local[0] + 2, local[1] + 2);

    //----Distribute global 2D-domain from rank 0 to all processes----//

 	//----Appropriate datatypes are defined here----//
	//----The usage of datatypes is optional----//

    //----Datatype definition for the 2D-subdomain on the global matrix----//
    MPI_Datatype global_block;
    MPI_Type_vector(local[0], local[1], global_padded[1], MPI_DOUBLE, &dummy);
    MPI_Type_create_resized(dummy, 0, sizeof(double), &global_block);
    MPI_Type_commit(&global_block);

    //----Datatype definition for the 2D-subdomain on the local matrix----//
    MPI_Datatype local_block;
    MPI_Type_vector(local[0], local[1], local[1] + 2, MPI_DOUBLE, &dummy);
    MPI_Type_create_resized(dummy, 0, sizeof(double), &local_block);
    MPI_Type_commit(&local_block);

    //----Rank 0 defines positions and counts of local blocks (2D-subdomains) on global matrix----//

    int *scatteroffset, *scattercounts;

    // We don't directly use &U[0][0] because U[0] is null for rank != 0
    double *U_start;

    if (rank == 0) {
        U_start = &U[0][0];

        scatteroffset = (int*) malloc(size * sizeof(int));
        scattercounts = (int*) malloc(size * sizeof(int));

        for (i = 0; i < grid[0]; i++)
            for (j = 0; j < grid[1]; j++) {
                scattercounts[i*grid[1] + j] = 1;
                scatteroffset[i*grid[1] + j] = local[0]*local[1]*grid[1]*i + local[1]*j;
            }
    }

    //----Rank 0 scatters the global matrix----//

	//********************DONE********************//

	/*
     * Fill your code here;
     *
     * Make sure u_current and u_previous are both initialized
     */

    MPI_Scatterv(U_start, scattercounts, scatteroffset, global_block, &u_previous[1][1], 1, local_block, 0, MPI_COMM_WORLD);
    MPI_Scatterv(U_start, scattercounts, scatteroffset, global_block, &u_current[1][1], 1, local_block, 0, MPI_COMM_WORLD);

    //********************************************//

    if (rank == 0)
        free2d(U);

	//----Define datatypes or allocate buffers for message passing----//

	//********************DONE********************//

	/* Fill your code here */

    MPI_Datatype row;
    MPI_Type_vector(local[1], 1, 1, MPI_DOUBLE, &row);
    MPI_Type_commit(&row);

    MPI_Datatype col;
    MPI_Type_vector(local[0], 1, local[1] + 2, MPI_DOUBLE, &col);
    MPI_Type_commit(&col);

	//********************************************//

    //----Find the 4 neighbors with which a process exchanges messages----//

	//********************DONE********************//

    int north, south, east, west;

	/*
     * Fill your code here;
     *
     * Make sure you handle non-existing neighbors appropriately
     */

    MPI_Cart_shift(CART_COMM, 0, 1, &north, &south);
    MPI_Cart_shift(CART_COMM, 1, 1, &west, &east);

	//********************************************//

    //----Define the iteration ranges per process-----//

	//********************DONE********************//

    int i_min, i_max, j_min, j_max;

	/*
     * Fill your code here;
     *
     * There are three types of ranges:
     *  -internal processes
     *  -boundary processes
     *  -boundary processes and padded global array
     */

    // Default to internal and change accordingly below
    i_min = 1;
    i_max = local[0];
    j_min = 1;
    j_max = local[1];

    // Top boundary; no padding
    if (north == MPI_PROC_NULL)
        i_min++;

    // Bottom boundary; may be padded
    if (south == MPI_PROC_NULL)
        i_max -= (global_padded[0] - global[0]) + 1;

    // Right boundary; may be padded
    if (east == MPI_PROC_NULL)
        j_max -= (global_padded[1] - global[1]) + 1;

    // Left boundary; no padding
    if (west == MPI_PROC_NULL)
        j_min++;

	//********************************************//

 	//----Computational core----//
    MPI_Barrier(MPI_COMM_WORLD);
	gettimeofday(&tts, NULL);

    #ifdef TEST_CONV
    for (t = 0; t < T && !global_converged; t++) {
    #endif
    #ifndef TEST_CONV
    #undef T
    #define T 256
    for (t = 0; t < T; t++) {
    #endif
	 	//********************DONE********************//

		/* Fill your code here */

		/* Communicate */
        MPI_Request requests[8];
        int req_cnt = 0;

        // No need for conditionals at the boundaries;
        // If no communication is needed (i.e. dest/source == MPI_PROC_NULL)
        // then the calls return as soon as possible
        // without any effect on the buffers

        // North
        MPI_Isend(&u_previous[1][1], 1, row, north, 0, MPI_COMM_WORLD, &requests[req_cnt++]);
        MPI_Irecv(&u_previous[0][1], 1, row, north, 0, MPI_COMM_WORLD, &requests[req_cnt++]);

        // South
        MPI_Isend(&u_previous[local[0]][1], 1, row, south, 0, MPI_COMM_WORLD, &requests[req_cnt++]);
        MPI_Irecv(&u_previous[local[0]+1][1], 1, row, south, 0, MPI_COMM_WORLD, &requests[req_cnt++]);

        // East
        MPI_Isend(&u_previous[1][local[1]], 1, col, east, 0, MPI_COMM_WORLD, &requests[req_cnt++]);
        MPI_Irecv(&u_previous[1][local[1]+1], 1, col, east, 0, MPI_COMM_WORLD, &requests[req_cnt++]);

        // West
        MPI_Isend(&u_previous[1][1], 1, col, west, 0, MPI_COMM_WORLD, &requests[req_cnt++]);
        MPI_Irecv(&u_previous[1][0], 1, col, west, 0, MPI_COMM_WORLD, &requests[req_cnt++]);

        MPI_Waitall(req_cnt, requests, MPI_STATUSES_IGNORE);

        /* Add appropriate timers for computation */
        gettimeofday(&tcs, NULL);

        /* Compute */
        for (i = i_min; i <= i_max; i++)
            for (j = j_min; j <= j_max; j++)
                u_current[i][j] = (u_previous[i-1][j] + u_previous[i+1][j] + u_previous[i][j-1] + u_previous[i][j+1]) / 4.0;

        gettimeofday(&tcf, NULL);

        tcomp += (tcf.tv_sec - tcs.tv_sec) + (tcf.tv_usec - tcs.tv_usec) * 0.000001;

		#ifdef TEST_CONV
        if (t % C == 0) {
			//********************DONE********************//

			/* Test convergence */
            gettimeofday(&tvs, NULL);

            converged = converge(u_previous, u_current, i_min, i_max, j_min, j_max);

            gettimeofday(&tvf, NULL);

            tconv += (tcf.tv_sec - tcs.tv_sec) + (tcf.tv_usec - tcs.tv_usec) * 0.000001;

            MPI_Allreduce(&converged, &global_converged, 1, MPI_INT, MPI_LAND, MPI_COMM_WORLD);

            //********************************************//
		}
		#endif

        swap = u_previous;
        u_previous = u_current;
        u_current = swap;

		//********************************************//
    }

    MPI_Barrier(MPI_COMM_WORLD);
    gettimeofday(&ttf, NULL);

    ttotal += (ttf.tv_sec - tts.tv_sec) + (ttf.tv_usec - tts.tv_usec) * 0.000001;

    MPI_Reduce(&ttotal, &total_time, 1, MPI_DOUBLE, MPI_MAX, 0, MPI_COMM_WORLD);
    MPI_Reduce(&tcomp, &comp_time, 1, MPI_DOUBLE, MPI_MAX, 0, MPI_COMM_WORLD);
    MPI_Reduce(&tconv, &conv_time, 1, MPI_DOUBLE, MPI_MAX, 0, MPI_COMM_WORLD);

    //----Rank 0 gathers local matrices back to the global matrix----//

    if (rank == 0)
        U = allocate2d(global_padded[0], global_padded[1]);

	//********************DONE********************//

	/* Fill your code here */

    if (rank == 0)
        U_start = &U[0][0];

    MPI_Gatherv(&u_current[1][1], 1, local_block, U_start, scattercounts, scatteroffset, global_block, 0, MPI_COMM_WORLD);

    //********************************************//

	//----Printing results----//

	//****DONE: Change "Jacobi" to "GaussSeidelSOR" or "RedBlackSOR" for appropriate printing****//
    if (rank == 0) {
        printf("Jacobi X %d Y %d Px %d Py %d Iter %d ComputationTime %lf ConvergenceTime %lf TotalTime %lf midpoint %lf\n",
            global[0], global[1], grid[0], grid[1], t, comp_time, conv_time, total_time, U[global[0] / 2][global[1] / 2]);

        #ifdef PRINT_RESULTS
        char *s = malloc(50 * sizeof(char));
        sprintf(s, "resJacobiMPI_%dx%d_%dx%d", global[0], global[1], grid[0], grid[1]);
        fprint2d(s, U, global[0], global[1]);
        free(s);
        #endif

    }
    MPI_Finalize();
    return 0;
}
