"""Synthetic cross-runtime parity and CLI ingestion regressions."""
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
import pandas as pd
from scripts.modules.clean_and_categorize import categorize_title, read_connections_csv
from scripts.modules.analyze_and_decide import action_recommendation
from scripts.modules.engagement_priority import compute_priority_score, assign_priority
from scripts.main import run_pipeline
from scripts.modules.excel_safety import safe_for_excel
from openpyxl import load_workbook

ROOT=Path(__file__).resolve().parents[1]

class ReleaseTests(unittest.TestCase):
    def test_excel_headers_are_text_and_quote_collisions_fail_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'synthetic.xlsx'
            frame=pd.DataFrame([{'Position':'Founder','=2+2':'synthetic',' +1':'synthetic'}])
            safe=safe_for_excel(frame)
            safe.to_excel(path,index=False)
            sheet=load_workbook(path).active
            self.assertEqual(sheet['B1'].data_type,'s')
            self.assertEqual(sheet['B1'].value,"'=2+2")
            self.assertEqual(sheet['C1'].data_type,'s')
            self.assertEqual(list(safe_for_excel(safe).columns),list(safe.columns))
            with self.assertRaisesRegex(ValueError,'headers collide'):
                safe_for_excel(pd.DataFrame([['a','b']],columns=['=2+2',"'=2+2"]))

    def test_python_javascript_fixture_parity(self):
        titles=['','Founder','Director','Production Supervisor','actor','Architecture','throughput',
                'Senior Product Manager','PM','Backend Engineer','CTO / Founder','HR AI Product Engineer',
                'DATA\tEngineer','ML','AI','Data','AI Engineer','hr','Human Resources','RECRUITER',
                'مدیر محصول','مهندس نرم‌افزار','développeur','产品经理','Productivity Coach',
                'Data-Engineer','Software_engineer','Software Engineer','Senior\u00a0Product Manager',
                'leadership','Recruitment Advisor',None]
        rows=[{'Position':title,'Company':company,'URL':url} for title in titles
              for company in ['', 'NA'] for url in ['', 'NULL']]
        expected=[]
        for row in rows:
            category=categorize_title(row['Position'])
            score=compute_priority_score(pd.Series({**row,'Category':category}))
            expected.append([category,score,assign_priority(score),action_recommendation(category)])
        script="const d=require('./docs/app.js');let s='';process.stdin.on('data',c=>s+=c);process.stdin.on('end',()=>process.stdout.write(JSON.stringify(d.analyze(JSON.parse(s)).map(r=>[r.category,r.score,r.priority,r.recommendation]))));"
        result=subprocess.run(['node','-e',script],input=json.dumps(rows),text=True,capture_output=True,cwd=ROOT,check=True)
        self.assertEqual(json.loads(result.stdout),expected)
        self.assertEqual(len(expected),128)

    def test_strict_csv_rejects_ragged_empty_header_and_invalid_utf8(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'synthetic.csv'
            for value in ['Position,Company\nA\n','Position\nA,B\n','Position,\nA,B\n','Position\n"unfinished']:
                path.write_text(value,encoding='utf-8')
                with self.assertRaises(ValueError):
                    read_connections_csv(path)
            path.write_bytes(b'Position\n\xff\n')
            with self.assertRaises(UnicodeError):
                read_connections_csv(path)

    def test_position_only_preamble_and_literal_na_survive_pipeline(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'synthetic.csv'
            path.write_text('\ufeffNotes: fictional\nPosition,Company,URL\nProduct Manager,NA,NULL\n',encoding='utf-8')
            out=Path(tmp)/'out'
            run_pipeline(path,out,'prioritize')
            result=pd.read_excel(out/'linkedin_priority.xlsx',keep_default_na=False)
            self.assertEqual(result.iloc[0]['Company'],'NA')
            self.assertEqual(result.iloc[0]['URL'],'NULL')
            self.assertEqual(result.iloc[0]['Priority Score'],8)

    def test_obsolete_category_file_removed_but_unrelated_files_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'synthetic.csv'
            out=Path(tmp)/'out'
            path.write_text('Position\nProduct Manager\n',encoding='utf-8')
            run_pipeline(path,out,'categorize')
            unrelated=out/'keep.txt'
            unrelated.write_text('synthetic',encoding='utf-8')
            path.write_text('Position\nFounder\n',encoding='utf-8')
            run_pipeline(path,out,'categorize')
            self.assertFalse((out/'Product.csv').exists())
            self.assertTrue(unrelated.exists())

    def test_input_cannot_be_overwritten_by_managed_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'all_connections_categorized.csv'
            path.write_text('Position\nFounder\n',encoding='utf-8')
            with self.assertRaises(ValueError):
                run_pipeline(path,tmp,'categorize')
            self.assertEqual(path.read_text(encoding='utf-8'),'Position\nFounder\n')

    def test_output_symlink_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            path=root/'synthetic.csv'
            path.write_text('Position\nFounder\n',encoding='utf-8')
            target=root/'real'
            target.mkdir()
            link=root/'linked'
            try:
                link.symlink_to(target,target_is_directory=True)
            except OSError:
                self.skipTest('Symlink creation unavailable')
            with self.assertRaises(ValueError):
                run_pipeline(path,link,'categorize')

