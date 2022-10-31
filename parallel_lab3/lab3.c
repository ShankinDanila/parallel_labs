#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

#define THREADS		8
#define	SIZE		1000000

int* Random_array(int rand_seed) {
	int* rand_arr = calloc(SIZE, sizeof(int));
	srand(rand_seed);

	for (int i = 0; i < SIZE; i++) { rand_arr[i] = rand(); }

	return rand_arr;
}

int* Wrong_array() {
	int* wrong_arr = calloc(SIZE, sizeof(int));
	
	for (int i = 0; i < SIZE; i++) { wrong_arr[i] = (SIZE - i); }
	return wrong_arr;
}

int* Correct_array(int rand_seed) {
	int* correct_arr = calloc(SIZE, sizeof(int));
		
	for (int i = 0; i < SIZE; i++) { correct_arr[i] = i; }
	
	srand(rand_seed);
	int magic_num = 1000; //0.2% from all elements willn't be in right order
	int tmp;

	for (int i = 0; i < magic_num; i++) {
		int target1, target2;
		target1 = rand() % SIZE;
		target2 = rand() % SIZE;
		tmp = correct_arr[target2];
		correct_arr[target2] = correct_arr[target1];
		correct_arr[target1] = tmp;
	}
	return correct_arr;
}

int* Strange_array(int rand_seed) {
	int* strange_arr = calloc(SIZE, sizeof(int));
	srand(rand_seed);

	int repeating_elem = rand();
	for (int i = 0; i < SIZE; i++) {
		if (i < SIZE / 2) { strange_arr[i] = repeating_elem; } //in the half of array we put random element
		else { strange_arr[i] = rand(); }
	}
	return strange_arr;
}

void InsertSort(int* arr, int i, int half, int* num_iteration){
	int temp = 0;
	int j = 0;

	for (int f = half + i; f < SIZE; f = f + half) {
		j = f;
		while(j > i && arr[j - half] > arr[j]) {
			temp = arr[j];
			arr[j] = arr[j - half];
			arr[j - half] = temp;
			*num_iteration += 1;
			j = j - half;
		}
	}
}

void ShellSort(int* array, float* times, int* iter) {
	int h;
	int i = 0;
	float t_start, t_end, t_total;
	for (int j = 0; j < THREADS; j++) {
		t_start = omp_get_wtime();
		for(h = SIZE/2; h > 0; h = h/2) {
			#pragma omp parallel num_threads(j + 1) shared(array, h, i, iter)  default(none)
			{
				#pragma omp for
				for(i = 0; i < h; i++) { InsertSort(array, i, h, iter); }
			}
		}
		t_end = omp_get_wtime();
		t_total = t_end - t_start;
		times[j] = t_total;
	}
}

int main(int argc, char** argv) {
	char* n_rand = argv[1];
	char* n_corr = argv[2];
	char* n_wrong = argv[3];
	char* n_strange = argv[4];

	FILE* f_rand = fopen(n_rand, "w");
	FILE* f_corr = fopen(n_corr, "w");
	FILE* f_wrong = fopen(n_wrong, "w");
	FILE* f_strange = fopen(n_strange, "w");

	int num_exec = 10;
	int rand_seed = 1337;
	int threads = THREADS;	

	unsigned int num_iter_rand = 0;
	unsigned int num_iter_corr = 0;
	unsigned int num_iter_wrong = 0;
	unsigned int num_iter_strange = 0;

	fwrite(&threads, sizeof(int), 1, f_rand);
	fwrite(&num_exec, sizeof(int), 1, f_rand);

	fwrite(&threads, sizeof(int), 1, f_corr);
	fwrite(&num_exec, sizeof(int), 1, f_corr);

	fwrite(&threads, sizeof(int), 1, f_wrong);
	fwrite(&num_exec, sizeof(int), 1, f_wrong);

	fwrite(&threads, sizeof(int), 1, f_strange);
	fwrite(&num_exec, sizeof(int), 1, f_strange);

	// random array
	unsigned int final_rand = 0;
	for (int i = 0; i < num_exec; i++) {
		float* times = (float*)calloc(THREADS, sizeof(float));
		int* arr_rand = Random_array(rand_seed + i);
		ShellSort(arr_rand, times, &num_iter_rand);
		final_rand += num_iter_rand;
		fwrite(times, sizeof(float), THREADS, f_rand);
		free(times);
		free(arr_rand);
	}
	final_rand /= num_exec;
	printf("For absolutely random array number of iterations = %d \n", final_rand);

	
	// correct order of array
	unsigned int final_corr = 0;
	for (int i = 0; i < num_exec; i++) {
		float* times = (float*)calloc(THREADS, sizeof(float));
		int* arr_correct = Correct_array(rand_seed + i);
		ShellSort(arr_correct, times, &num_iter_corr);
		final_corr += num_iter_corr;
		fwrite(times, sizeof(float), THREADS, f_corr);
		free(times);
		free(arr_correct);
	}
	final_corr /= num_exec;
	printf("For almost correct ordered array number of iterations = %d \n", final_corr);


	// wrong order array
	unsigned int final_wrong = 0;
	for (int i = 0; i < num_exec; i++) {
		float* times = (float*)calloc(THREADS, sizeof(float));
		int* arr_wrong = Wrong_array();
		ShellSort(arr_wrong, times, &num_iter_wrong);
		final_wrong += num_iter_wrong;
		fwrite(times, sizeof(float), THREADS, f_wrong);
		free(times);
		free(arr_wrong);
	}
	final_wrong /= num_exec;
	printf("For wrong ordered array number of iterations = %d \n", final_wrong);


	// strange order of array
	unsigned int final_strange = 0;
	for (int i = 0; i < num_exec; i++) {
		float* times = (float*)calloc(THREADS, sizeof(float));
		int* arr_strange = Strange_array(rand_seed + i);
		ShellSort(arr_strange, times, &num_iter_strange);
		final_strange += num_iter_strange;
		fwrite(times, sizeof(float), THREADS, f_strange);
		free(times);
		free(arr_strange);
	}
	final_strange /= num_exec;
	printf("For 'strange' array number of iterations = %d \n", final_strange);


	fclose(f_rand);
	fclose(f_corr);
	fclose(f_wrong);
	fclose(f_strange);

	return 0;
}
