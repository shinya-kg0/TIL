import { Box, Card, CardBody, CardHeader, Button, ChakraProvider, Checkbox, Flex, Input, Text } from '@chakra-ui/react'
import './App.css'
import { useState } from 'react'

type Record = {
  id: number
  title: string
  isIncome: boolean
  amount: number
}

function App() {
  const [records, setRecords] = useState<Record[]>([])
  const [title, setTitle] = useState<string>("")
  const [isIncome, setIsIncome] = useState<boolean>(false)
  const [amount, setAmount] = useState<number>(0)

  const handleRecords = () => {
    setRecords([...records, 
      {id: records.length + 1, "title": title, "isIncome": isIncome, "amount": amount}])
    setTitle("")
    setAmount(0)
    setIsIncome(false)
    }
  

  return (
    <ChakraProvider>
      <Box display="flex" justifyContent="center" alignItems="center">
        <Card width="80%">
          <CardHeader>
            <Text fontSize="2xl">家計簿アプリ</Text>
          </CardHeader>
          <CardBody>
            <div>
              <Input placeholder='タイトルを入力'mb="4px" value={title} onChange={(e) => setTitle(e.target.value)} />
              <Input placeholder='支出を入力' mb="4px" value={amount} onChange={(e) => setAmount(Number(e.target.value))} />
              <Flex align="center" justifyContent="space-between">
                <Checkbox w="100px" isChecked={isIncome} onChange={() => setIsIncome(!isIncome)}>入金</Checkbox>
                <Button colorScheme='teal' onClick={handleRecords}>追加</Button>
              </Flex>
            </div>
            <div>
              {records.map((data) => (
                <div key={data.id}>
                  <Flex align="center" justifyContent="space-between">
                    <Text>{data.title}</Text>
                    <Text>{data.isIncome ? "+" : "-"}{data.amount}</Text>
                  </Flex>
                </div>
              ))}

            </div>
          </CardBody>
        </Card>
      </Box>
    </ChakraProvider>

  )
}

export default App
