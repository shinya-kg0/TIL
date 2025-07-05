import { Box, Card, CardBody, CardHeader, Button, ChakraProvider, Checkbox, Flex, Input, Text } from '@chakra-ui/react'
import './App.css'


function App() {


  return (
    <ChakraProvider>
      <Box display="flex" justifyContent="center" alignItems="center">
        <Card width="80%">
          <CardHeader>
            <Text fontSize="2xl">家計簿アプリ</Text>
          </CardHeader>
          <CardBody>
            <div>
              <Input placeholder='支出を入力' mb="4px" />
              <Flex align="center" justifyContent="space-between">
                <Checkbox w="100px">入金</Checkbox>
                <Button colorScheme='teal'>追加</Button>
              </Flex>
            </div>
          </CardBody>
        </Card>
      </Box>
    </ChakraProvider>

  )
}

export default App
