import tempfile, unittest
from app import PromptRegistry, compare_fixtures
class PromptRegistryTests(unittest.TestCase):
    def test_versions_are_immutable_and_ordered(self):
        with tempfile.TemporaryDirectory() as tmp:
            registry=PromptRegistry(tmp+"/test.db")
            registry.save("support","Answer briefly.")
            registry.save("support","Answer briefly and cite sources.")
            self.assertEqual(registry.get("support",1)["body"],"Answer briefly.")
            self.assertEqual([x["version"] for x in registry.history("support")],[1,2])
    def test_empty_prompt_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError): PromptRegistry(tmp+"/test.db").save("","x")
    def test_fixture_diff(self):
        result=compare_fixtures([{"id":"a","expected":"yes"}],[{"id":"a","expected":"no"},{"id":"b","expected":"ok"}])
        self.assertEqual(len(result["changed_cases"]),2); self.assertEqual(result["regression_count"],1)
if __name__=="__main__": unittest.main()
