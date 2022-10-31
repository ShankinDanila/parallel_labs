export OMP_CANCELLATION = true
#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

int threads = 8;

void function(int rand_seed, float *times){

    const int count = 10000000; ///< Number of array elements
    int *array = calloc(count, sizeof(int)); ///< The array we need to find the max in
    int target,flag;
    float start_time = 0, end_time = 0;
    srand(rand_seed);
    for(int i=0; i<count; i++) { array[i] = rand(); }
    for(int i = 0; i < threads; i++) {
        target = rand() % count;
        start_time = omp_get_wtime();
        #pragma omp parallel num_threads(i + 1) shared(array, count, i, target, flag) default(none) 
		{
             #pragma omp for
             for(int j = 0; j < count; j++) {
                 if(array[j] == target) { 
				     #pragma omp cancel for	  
				 }
				 #pragma omp cancellation point for
			 }
		}
        end_time = omp_get_wtime();
        times[i] = end_time - start_time;
	}
    free(array);
}

int main(int argc, char** argv){
    int iter = 10;
    int threads = 8;
    int seed = 93932;
    FILE *file = fopen("data_cancel.txt", "w");
    fwrite(&threads, sizeof(int), 1, file);
    fwrite(&iter, sizeof(int), 1, file);
    float *times = 0;
    for(int i = 0; i < iter; i++){
        times = (float*)calloc(threads, sizeof(float));
        function(seed + i, times);
        fwrite(times, sizeof(float), threads, file);
        free(times);
    }
    fclose(file);
    return 0;
}
