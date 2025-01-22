import struct
from typing import Tuple, List, Optional

from app.schemas.stdf import MasterInfo, PartResult, TestResult, STDFData


class STDFDecoder:
    @staticmethod
    def decode_mir(data: bytes, offset: int) -> Tuple[MasterInfo, int]:
        header = data[offset:offset + 3]
        if header != b'MIR':
            raise ValueError(f"Invalid MIR header: {header}")

        temperature, = struct.unpack('f', data[offset + 4:offset + 8])
        operator_name = data[offset + 8:offset + 28].decode('ascii').strip('\x00')

        return MasterInfo(
            temperature=temperature,
            operator_name=operator_name
        ), offset + 28

    @staticmethod
    def decode_prr(data: bytes, offset: int) -> Tuple[PartResult, int]:
        header = data[offset:offset + 3]
        if header != b'PRR':
            raise ValueError(f"Invalid PRR header: {header}")

        part_number, = struct.unpack('i', data[offset + 4:offset + 8])
        passed = data[offset + 8:offset + 9][0] == 1

        return PartResult(
            part_number=part_number,
            passed=passed,
            tests=[]
        ), offset + 9

    @staticmethod
    def decode_ptr(data: bytes, offset: int) -> Tuple[TestResult, int]:
        header = data[offset:offset + 3]
        if header != b'PTR':
            raise ValueError(f"Invalid PTR header: {header}")

        test_name = data[offset + 4:offset + 24].decode('ascii').strip('\x00')
        test_value, low_limit, high_limit = struct.unpack('fff', data[offset + 24:offset + 36])
        passed = data[offset + 36:offset + 37][0] == 1

        return TestResult(
            test_name=test_name,
            test_value=test_value,
            low_limit=low_limit,
            high_limit=high_limit,
            passed=passed
        ), offset + 37

    @classmethod
    def decode_file(cls, file_data: bytes) -> STDFData:
        offset = 0
        mir, offset = cls.decode_mir(file_data, offset)

        parts: List[PartResult] = []
        current_part: Optional[PartResult] = None

        while offset < len(file_data):
            header = file_data[offset:offset + 3]

            if header == b'PRR':
                if current_part:
                    parts.append(current_part)
                current_part, offset = cls.decode_prr(file_data, offset)

            elif header == b'PTR':
                if current_part is None:
                    raise ValueError("PTR record without PRR")
                ptr, offset = cls.decode_ptr(file_data, offset)
                current_part.tests.append(ptr)

            else:
                offset += 1

        if current_part:
            parts.append(current_part)

        return STDFData(mir=mir, parts=parts)
