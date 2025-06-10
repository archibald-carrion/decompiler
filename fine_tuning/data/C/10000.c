#ifndef WRAPPER_H_
#define WRAPPER_H_

#ifdef __cplusplus
extern "C" {
#endif

void *person_create(const char *, int);
void person_destroy(void *);
int person_get_age(void *);
const char *person_get_name(void *);

#ifdef __cplusplus
}
#endif

#endif // WRAPPER_H_