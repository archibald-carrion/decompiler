#ifndef FOOLIB_C_H
#define FOOLIB_C_H 1

#ifdef __cplusplus
extern "C" {
#endif

#include <stdint.h>

typedef int foolib_result_t;
#define FOOLIB_RESULT_SUCCESS 0
#define FOOLIB_RESULT_ERROR_ALLOC_FAILED 101
#define FOOLIB_RESULT_ERROR_BAD_STATE 102
#define FOOLIB_RESULT_ERROR_NOT_FOUND 103

typedef int foolib_object_t;
#define FOOLIB_OBJECT_ALLOC_FAILED 0

extern int foolib_g_verbosity;

foolib_result_t foolib_g_init();
foolib_result_t foolib_g_destroy();

foolib_object_t foolib_new();
foolib_result_t foolib_delete(foolib_object_t object);
foolib_result_t foolib_operation(foolib_object_t object);

#ifdef __cplusplus
}
#endif

#endif
