from typing import List

from pydantic import BaseModel


class TestResult(BaseModel):
    test_name: str
    test_value: float
    low_limit: float
    high_limit: float
    passed: bool


class PartResult(BaseModel):
    part_number: int
    passed: bool
    tests: List[TestResult]


class MasterInfo(BaseModel):
    temperature: float
    operator_name: str


class STDFData(BaseModel):
    mir: MasterInfo
    parts: List[PartResult]
