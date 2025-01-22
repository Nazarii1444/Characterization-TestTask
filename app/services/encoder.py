import struct

from app.schemas.stdf import STDFData, PartResult, TestResult, MasterInfo


class STDFEncoder:
    @staticmethod
    def encode_mir(mir: MasterInfo) -> bytes:
        header = b'MIR\x00'
        temperature = struct.pack('f', mir.temperature)
        operator = mir.operator_name.encode('ascii').ljust(20, b'\x00')
        return header + temperature + operator

    @staticmethod
    def encode_prr(prr: PartResult) -> bytes:
        header = b'PRR\x00'
        part_number = struct.pack('i', prr.part_number)
        passed = bytes([1 if prr.passed else 0])
        return header + part_number + passed

    @staticmethod
    def encode_ptr(ptr: TestResult) -> bytes:
        header = b'PTR\x00'
        test_name = ptr.test_name.encode('ascii').ljust(20, b'\x00')
        values = struct.pack('fff', ptr.test_value, ptr.low_limit, ptr.high_limit)
        passed = bytes([1 if ptr.passed else 0])
        return header + test_name + values + passed

    @classmethod
    def encode_data(cls, data: STDFData) -> bytes:
        result = bytearray(cls.encode_mir(data.mir))

        for part in data.parts:
            result.extend(cls.encode_prr(part))
            for test in part.tests:
                result.extend(cls.encode_ptr(test))

        return bytes(result)
