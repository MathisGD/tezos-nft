#imported from FA2 to facilitate transfers
class Simple_batch_transfer:
  
    def get_transfer_type(self):
        tx_type = sp.TRecord(to_ = sp.TAddress,
                             token_id = token_id_type,
                             amount = sp.TNat)

        tx_type = tx_type.layout(
                ("to_", ("token_id", "amount"))
            )
        transfer_type = sp.TRecord(from_ = sp.TAddress,
                                   txs = sp.TList(tx_type)).layout(
                                       ("from_", "txs"))
        return transfer_type
    def get_type(self):
        return sp.TList(self.get_transfer_type())
    def item(self, from_, txs):
        v = sp.record(from_ = from_, txs = txs)
        return sp.set_type_expr(v, self.get_transfer_type())

class Locker(sp.Contract):
    
    def __init__(self,nft_contract_address, admin_address):
        self.init(tokens = sp.map(),total_tokens = sp.int(0),admin_address = admin_address,
        nft_contract = nft_contract_address)
        self.batch_transfer = Simple_batch_transfer()

    
    @sp.entry_point
    def deposit(self, address_from, contract_address, token_id):


        sp.verify(~ self.data.tokens.contains(token_id),message="Token already deposited")

        batch_type = self.batch_transfer.get_type()
        transfer_point = sp.contract(batch_type, self.data.nft_contract, entry_point = "transfer").open_some()
        data_to_send = [self.batch_transfer.item(from_ = sp.sender, txs = [ sp.record(to_ = self.address ,amount = 1,token_id = token_id)])]
            
        sp.transfer(data_to_send, sp.mutez(0), transfer_point)

        self.data.tokens[token_id] = sp.record(owner=sp.set_type_expr(address_from,sp.TAddress), 
                                        contract=sp.set_type_expr(contract_address,sp.TAddress),
                                        token_id=sp.set_type_expr(token_id,sp.TNat),
                                        status="deposited")
        self.data.total_tokens +=1

        #sp.result(self.data.total_tokens)
        
    @sp.entry_point
    def lockToken(self, token_id):
        
        sp.verify(self.data.tokens.contains(token_id),message="Token not deposited")
        sp.verify(~ (self.data.tokens[token_id].status == "locked"),"Token already locked")
        sp.verify(sp.sender == self.data.tokens[token_id].owner,"Only owner can lock token")

        self.data.tokens[token_id].status = "locked"

    @sp.entry_point
    def unlockToken(self, token_id):
        sp.verify(self.data.tokens.contains(token_id),"Token not found") 
        sp.verify(sp.sender == self.data.tokens[token_id].owner, "Only owner can unlock")
        
        sp.verify(~ (self.data.tokens[token_id].status == "unlocked"),"Token already unlocked")

        self.data.tokens[token_id].status = "unlocked"

    @sp.entry_point
    def withdraw(self, token_id):
        sp.verify(self.data.tokens.contains(token_id),"Token not found") 
        sp.verify(sp.sender == self.data.tokens[token_id].owner,"Only owner can withdraw")
        sp.verify(self.data.tokens[token_id].status == "unlocked","Unlock token before withadraw")

        batch_type = self.batch_transfer.get_type()
        transfer_point = sp.contract(batch_type, self.data.nft_contract, entry_point = "transfer").open_some()

        data_to_send = [self.batch_transfer.item(from_ = self.address, txs = [ sp.record(to_ = sp.sender,amount = 1,token_id = token_id)])]
            
        sp.transfer(data_to_send, sp.mutez(0), transfer_point)
        del self.data.tokens[token_id]
        self.data.total_tokens -= 1


