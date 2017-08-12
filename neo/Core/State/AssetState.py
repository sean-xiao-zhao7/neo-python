
from .StateBase import StateBase
import sys
import binascii
from neo.Fixed8 import Fixed8
from neo.IO.BinaryReader import BinaryReader
from neo.IO.BinaryWriter import BinaryWriter
from neo.IO.MemoryStream import MemoryStream,StreamManager
from neo.Core.AssetType import AssetType

class AssetState(StateBase):


    AssetId = None
    AssetType = None
    Name = None
    Amount = Fixed8(0)
    Available = Fixed8(0)
    Precision = 0
    FeeMode = 0
    Fee = Fixed8(0)
    FeeAddress = None
    Owner = None
    Admin = None
    Issuer = None
    Expiration = None
    IsFrozen = False


    def __init__(self, asset_id=None, asset_type=None,name=None,amount=Fixed8(0),available=Fixed8(0),
                 precision=0, fee_mode=0, fee=Fixed8(0), fee_addr=None, owner=None,
                 admin=None,issuer=None,expiration=None,is_frozen=False):
        self.AssetId = asset_id
        self.AssetType = asset_type
        self.Name = name
        self.Amount = amount
        self.Available = available
        self.Precision = precision
        self.FeeMode = fee_mode
        self.Fee = fee
        self.FeeAddress = fee_addr
        self.Owner = owner
        self.Admin = admin
        self.Issuer = issuer
        self.Expiration = expiration
        self.IsFrozen = is_frozen

#    def Size(self):
#        return super(AssetState, self).Size()

    @staticmethod
    def DeserializeFromDB(buffer):
        m = StreamManager.GetStream(buffer)
        reader = BinaryReader(m)
        account = AssetState()
        account.Deserialize(reader)

        StreamManager.ReleaseStream(m)

        return account

    def Deserialize(self, reader):
        super(AssetState, self).Deserialize(reader)
        self.AssetId = reader.ReadUInt256()
        self.AssetType = reader.ReadByte()
        self.Name = reader.ReadVarString()
        self.Amount = reader.ReadFixed8()
        self.Available = reader.ReadFixed8()
        self.Precision = reader.ReadByte()
        #fee mode
        reader.ReadByte()

        self.Fee = reader.ReadFixed8()
        self.FeeAddress = reader.ReadUInt160()
        self.Owner = reader.ReadBytes(33)
        self.Admin = reader.ReadUInt160()
        self.Issuer = reader.ReadUInt160()
        self.Expiration = reader.ReadUInt32()
        self.IsFrozen = reader.ReadBool()

    def Serialize(self, writer):
        super(AssetState, self).Serialize(writer)
        writer.WriteUInt256( self.AssetId)
        writer.WriteByte(self.AssetType)
        writer.WriteVarString(self.Name)
        writer.WriteFixed8(self.Amount)
        writer.WriteFixed8(self.Available)
        writer.WriteByte(self.Precision)
        writer.WriteByte(self.FeeMode)
        writer.WriteFixed8(self.Fee)
        writer.WriteUInt160(self.FeeAddress)
        writer.WriteBytes(self.Owner)
        writer.WriteUInt160(self.Admin)
        writer.WriteUInt160(self.Issuer)
        writer.WriteUInt32(self.Expiration)
        writer.WriteBool(self.IsFrozen)

    def GetName(self):
        if self.AssetType == AssetType.AntShare: return "NEO"
        elif self.AssetType == AssetType.AntCoin: return "NEOGas"

        return "Name!"
