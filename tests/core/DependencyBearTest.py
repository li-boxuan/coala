from concurrent.futures import ThreadPoolExecutor

from coalib.core.DependencyBear import DependencyBear
from coalib.core.FileBear import FileBear
from coalib.core.ProjectBear import ProjectBear
from coalib.settings.Section import Section

from tests.core.CoreTestBase import CoreTestBase


class TestProjectBear(ProjectBear):

    def analyze(self, files):
        yield ', '.join('{}({})'.format(filename, len(files[filename]))
                        for filename in sorted(files))


class TestFileBear(FileBear):

    def analyze(self, filename, file):
        yield '{}:{}'.format(filename, len(file))


class TestBearDependentOnProjectBear(DependencyBear):
    BEAR_DEPS = {TestProjectBear}

    def analyze(self, dependency_bear, dependency_result):
        yield '{} - {}'.format(dependency_bear.name, dependency_result)


class TestBearDependentOnFileBear(DependencyBear):
    BEAR_DEPS = {TestFileBear}

    def analyze(self, dependency_bear, dependency_result):
        yield '{} - {}'.format(dependency_bear.name, dependency_result)


class TestBearDependentOnMultipleBears(DependencyBear):
    BEAR_DEPS = {TestFileBear, TestProjectBear}

    def analyze(self, dependency_bear, dependency_result, a_number=100):
        yield '{} ({}) - {}'.format(
            dependency_bear.name, a_number, dependency_result)


class DependencyBearTest(CoreTestBase):

    def assertResultsEqual(self, bear_type, expected,
                           section=None, file_dict=None):
        """
        Asserts whether the expected results do match the output of the bear.

        Asserts for the results out-of-order.

        :param bear_type:
            The bear class to check.
        :param expected:
            A sequence of expected results.
        :param section:
            A section for the bear to use. By default uses a new section with
            name ``test-section``.
        :param file_dict:
            A file-dictionary for the bear to use. By default uses an empty
            dictionary.
        """
        if section is None:
            section = Section('test-section')
        if file_dict is None:
            file_dict = {}

        uut = bear_type(section, file_dict)

        results = self.execute_run({uut})

        self.assertEqual(sorted(expected), sorted(results))

    def test_projectbear_dependency(self):
        # Dependency results are also catched in the result callback, thus they
        # are included in the final result list.
        self.assertResultsEqual(
            TestBearDependentOnProjectBear,
            file_dict={},
            expected=['',
                      'TestProjectBear - '])
        self.assertResultsEqual(
            TestBearDependentOnProjectBear,
            file_dict={'fileX': []},
            expected=['fileX(0)',
                      'TestProjectBear - fileX(0)'])
        self.assertResultsEqual(
            TestBearDependentOnProjectBear,
            file_dict={'fileX': [], 'fileY': ['hello']},
            expected=['fileX(0), fileY(1)',
                      'TestProjectBear - fileX(0), fileY(1)'])
        self.assertResultsEqual(
            TestBearDependentOnProjectBear,
            file_dict={'fileX': [], 'fileY': ['hello'], 'fileZ': ['x\n', 'y']},
            expected=['fileX(0), fileY(1), fileZ(2)',
                      'TestProjectBear - fileX(0), fileY(1), fileZ(2)'])

    def test_filebear_dependency(self):
        # Dependency results are also catched in the result callback, thus they
        # are included in the final result list.
        self.assertResultsEqual(
            TestBearDependentOnFileBear,
            file_dict={},
            expected=[])
        self.assertResultsEqual(
            TestBearDependentOnFileBear,
            file_dict={'fileX': []},
            expected=['fileX:0',
                      'TestFileBear - fileX:0'])
        self.assertResultsEqual(
            TestBearDependentOnFileBear,
            file_dict={'fileX': [], 'fileY': ['hello']},
            expected=['fileX:0',
                      'fileY:1',
                      'TestFileBear - fileX:0',
                      'TestFileBear - fileY:1'])
        self.assertResultsEqual(
            TestBearDependentOnFileBear,
            file_dict={'fileX': [], 'fileY': ['hello'], 'fileZ': ['x\n', 'y']},
            expected=['fileX:0',
                      'fileY:1',
                      'fileZ:2',
                      'TestFileBear - fileX:0',
                      'TestFileBear - fileY:1',
                      'TestFileBear - fileZ:2'])

    def test_multiple_bears_dependencies(self):
        # Dependency results are also catched in the result callback, thus they
        # are included in the final result list.
        self.assertResultsEqual(
            TestBearDependentOnMultipleBears,
            file_dict={},
            expected=['',
                      'TestProjectBear (100) - '])
        self.assertResultsEqual(
            TestBearDependentOnMultipleBears,
            file_dict={'fileX': []},
            expected=['fileX(0)',
                      'TestProjectBear (100) - fileX(0)',
                      'fileX:0',
                      'TestFileBear (100) - fileX:0'])
        self.assertResultsEqual(
            TestBearDependentOnMultipleBears,
            file_dict={'fileX': [], 'fileY': ['hello']},
            expected=['fileX(0), fileY(1)',
                      'TestProjectBear (100) - fileX(0), fileY(1)',
                      'fileX:0',
                      'fileY:1',
                      'TestFileBear (100) - fileX:0',
                      'TestFileBear (100) - fileY:1'])
        self.assertResultsEqual(
            TestBearDependentOnMultipleBears,
            file_dict={'fileX': [], 'fileY': ['hello'], 'fileZ': ['x\n', 'y']},
            expected=['fileX(0), fileY(1), fileZ(2)',
                      'TestProjectBear (100) - fileX(0), fileY(1), fileZ(2)',
                      'fileX:0',
                      'fileY:1',
                      'fileZ:2',
                      'TestFileBear (100) - fileX:0',
                      'TestFileBear (100) - fileY:1',
                      'TestFileBear (100) - fileZ:2'])

    def test_multiple_bears_dependencies_with_parameter(self):
        section = Section('test-section')
        section['a_number'] = '500'

        # Dependency results are also catched in the result callback, thus they
        # are included in the final result list.
        self.assertResultsEqual(
            TestBearDependentOnMultipleBears,
            section=section,
            file_dict={},
            expected=['',
                      'TestProjectBear (500) - '])
        self.assertResultsEqual(
            TestBearDependentOnMultipleBears,
            section=section,
            file_dict={'fileX': []},
            expected=['fileX(0)',
                      'TestProjectBear (500) - fileX(0)',
                      'fileX:0',
                      'TestFileBear (500) - fileX:0'])
        self.assertResultsEqual(
            TestBearDependentOnMultipleBears,
            section=section,
            file_dict={'fileX': [], 'fileY': ['hello']},
            expected=['fileX(0), fileY(1)',
                      'TestProjectBear (500) - fileX(0), fileY(1)',
                      'fileX:0',
                      'fileY:1',
                      'TestFileBear (500) - fileX:0',
                      'TestFileBear (500) - fileY:1'])
        self.assertResultsEqual(
            TestBearDependentOnMultipleBears,
            section=section,
            file_dict={'fileX': [], 'fileY': ['hello'], 'fileZ': ['x\n', 'y']},
            expected=['fileX(0), fileY(1), fileZ(2)',
                      'TestProjectBear (500) - fileX(0), fileY(1), fileZ(2)',
                      'fileX:0',
                      'fileY:1',
                      'fileZ:2',
                      'TestFileBear (500) - fileX:0',
                      'TestFileBear (500) - fileY:1',
                      'TestFileBear (500) - fileZ:2'])


# Execute the same tests from DependencyBearTest, but use a ThreadPoolExecutor
# instead. It shall also seamlessly work with Python threads. Also there are
# coverage issues on Windows with ProcessPoolExecutor as coverage data isn't
# passed properly back from the pool processes.
class DependencyBearOnThreadPoolExecutorTest(DependencyBearTest):
    def setUp(self):
        super().setUp()
        self.executor = ThreadPoolExecutor, tuple(), dict(max_workers=8)

    # Cache-tests require to be executed in the same Python process, as mocks
    # aren't multiprocessing capable. Thus put them here.

    def test_cache(self):
        # TODO TBD (especially test dependency caching!)
        """
        section = Section('test-section')
        filedict1 = {'file.txt': []}
        filedict2 = {'file.txt': ['first-line\n'], 'file2.txt': ['xyz\n']}
        filedict3 = {'file.txt': ['first-line\n'], 'file2.txt': []}
        cache = {}

        # Due to https://bugs.python.org/issue31807#msg306273, we can't use
        # `autospec=True` together with `wraps`, `wraps` simply doesn't have
        # any effect. This means we can't nicely use `self.assertResultsEqual`
        # here. But we aren't actually interested in the results returned by
        # the bear, we just want to be sure that the cache works and properly
        # calls / doesn't call `analyze()`.

        with patch.object(TestFileBear, 'analyze',
                          autospec=True,
                          return_value=[]) as mock:

            uut = TestFileBear(section, filedict1, cache)
            self.execute_run({uut})

            mock.assert_called_once_with(ANY, *next(iter(filedict1.items())))
            assert len(cache) == 1

        with patch.object(TestFileBear, 'analyze',
                          autospec=True,
                          return_value=[]) as mock:

            uut = TestFileBear(section, filedict2, cache)
            self.execute_run({uut})

            assert mock.call_count == 2
            for filename, file in filedict2.items():
                mock.assert_any_call(ANY, filename, file)
            assert len(cache) == 3

        with patch.object(TestFileBear, 'analyze',
                          autospec=True,
                          return_value=[]) as mock:

            uut = TestFileBear(section, filedict3, cache)
            self.execute_run({uut})

            mock.assert_called_once_with(ANY, 'file2.txt', [])
            assert len(cache) == 4
        """
