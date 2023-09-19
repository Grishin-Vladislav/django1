import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from model_bakery import baker

from students.models import Course, Student


@pytest.fixture(scope='module')
def client():
    return APIClient()


@pytest.fixture
def courses_factory():
    def courses(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return courses


@pytest.fixture
def courses_factory_prepare():
    def courses(*args, **kwargs):
        return baker.prepare(Course, *args, **kwargs)

    return courses


@pytest.mark.django_db
def test_get_certain_course(client, courses_factory):
    course = courses_factory()
    # #
    #     from django import urls
    #
    #     url_resolver = urls.get_resolver(urls.get_urlconf())
    #     print(url_resolver.namespace_dict.items())
    #
    url = reverse('courses-list')
    response = client.get(
        f'/api/v1/courses/{course.id}/'
    )

    assert response.status_code == 200
    assert response.json()['name'] == course.name


@pytest.mark.django_db
def test_get_courses_list(client, courses_factory):
    courses = courses_factory(_quantity=100)

    response = client.get(f'/api/v1/courses/')

    assert response.status_code == 200
    for index, course in enumerate(response.json()):
        assert course['name'] == courses[index].name


@pytest.mark.django_db
def test_filter_by_id(client, courses_factory):
    courses = courses_factory(_quantity=10)

    for course in courses:
        response = client.get(f'/api/v1/courses/?id={course.id}')
        data = response.json()

        assert response.status_code == 200
        assert len(data) == 1
        assert data[0]['name'] == course.name


@pytest.mark.django_db
def test_filter_by_name(client, courses_factory):
    courses = courses_factory(_quantity=10)

    for course in courses:
        response = client.get(f'/api/v1/courses/?name={course.name}')
        data = response.json()

        assert response.status_code == 200
        assert len(data) == 1
        assert data[0]['name'] == course.name


@pytest.mark.django_db
def test_create_course(client, courses_factory_prepare):
    courses = courses_factory_prepare(_quantity=2)

    for course in courses:
        data = {
            'name': course.name,
            'students': []
        }

        response = client.post('/api/v1/courses/', data=data,
                               format='json')
        assert response.status_code == 201

        course_db = Course.objects.filter(name=data['name']).first()

        assert course_db
        assert list(course_db.students.all()) == data['students']

    assert Course.objects.count() == len(courses)


@pytest.mark.django_db
def test_update_course(client, courses_factory):
    course = courses_factory()
    data = {'name': 'python'}

    response = client.patch(f'/api/v1/courses/{course.id}/',
                            data=data,
                            format='json')

    assert response.status_code == 200
    assert response.json()['name'] == data['name']


@pytest.mark.django_db
def test_destroy_course(client, courses_factory):
    course = courses_factory()

    response = client.delete(f'/api/v1/courses/{course.id}/')

    assert response.status_code == 204
    assert Course.objects.count() == 0
