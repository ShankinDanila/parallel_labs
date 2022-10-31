#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

void fu(int rand_seed, float* times)
{
    const int count = 10000000;     ///< Number of array elements
    const int threads = 8;         ///< Number of parallel threads to use
   
    int* array = 0;                 ///< The array we need to find the max in
    
    /* Initialize the RNG */
    srand(rand_seed);

    /* Generate the random array */
    array = (int*)malloc(count*sizeof(int));
    for(int i=0; i<count; i++) { array[i] = rand(); }
	
	for (int i = 0; i < threads; i++) {
	
		int max = -1;

		float t_start = 0, t_end = 0; 
		t_start = omp_get_wtime();

		#pragma omp parallel num_threads(i + 1) shared(array, count, i) reduction(max: max) default(none)
		{
			#pragma omp for
			for(int j=0; j < count; j++)
			{
				if(array[j] > max) { max = array[j]; };
			}
		}
		t_end = omp_get_wtime();
		times[i] = t_end - t_start;
	}

	free(array);
}


int main(int argc, char** argv){
	
	int iter = 10;
	int random_seed = 920215; ///< RNG seed
	int threads = 8;
	FILE *file = fopen("data.txt", "w");

	fwrite(&threads, sizeof(int), 1, file);
	fwrite(&iter, sizeof(int), 1, file);
	float* times = 0;

	for (int i = 0; i < 10; i++) {
		times = (float*)calloc(threads, sizeof(float));
		fu(random_seed + i, times);
		fwrite(times, sizeof(float), threads, file);
		free(times);
	}
	
	fclose(file);
	return 0;
}

